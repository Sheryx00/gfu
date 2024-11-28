import os
import json
import time
import argparse
import random
import requests
import re

# Colors for terminal output
BLUE = "\33[94m"
RED = "\33[91m"
END = "\033[0m"

# Default location for JSON pattern files
PATTERN_FOLDER = os.path.expanduser("~/.gfu")

# List of most commonly used User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.67"
]

def load_pattern_file(pattern_name):
    """
    Loads the JSON file for the specified pattern from the pattern folder.
    """
    pattern_file = os.path.join(PATTERN_FOLDER, f"{pattern_name}.json")
    if not os.path.exists(pattern_file):
        raise FileNotFoundError(f"{RED}Pattern file not found:{END} {pattern_file}")
    
    with open(pattern_file, "r") as f:
        return json.load(f)

def build_queries(pattern_data, target):
    """
    Constructs the search queries using the templates from the pattern JSON.
    """
    templates = pattern_data.get("templates", [])
    return [template.replace("{target}", target) for template in templates]

def is_valid_file_url(url, valid_sites):
    """
    Validates whether a URL points to a file hosted on one of the specified valid sites.
    """
    if not valid_sites:
        return True  # No valid_sites specified; accept all URLs
    return any(site in url for site in valid_sites)

def google_dork_search(queries, delay, output_folder, pattern_name, max_pages=50, results_per_page=10):
    """
    Performs Google dork searches for the given queries.
    :param queries: List of queries to search for.
    :param delay: Delay (in seconds) between requests.
    :param output_folder: Folder where the log file is stored.
    :param pattern_name: Name of the pattern being searched.
    :param max_pages: Maximum number of pages to fetch.
    :param results_per_page: Number of results to fetch per page (max 100).
    """
    all_urls = []
    exclude_domains = [
        "google.com",
        "webcache.googleusercontent.com",
        "www.gstatic.com",
        "search.app.goo.gl",
        "www.google.se",
    ]
    
    log_file = os.path.join(output_folder, "gfu.log")

    # Add header for the pattern
    with open(log_file, "a") as f:
        f.write(f"# {pattern_name}\n")

    for query in queries:
        print(f"{BLUE}Searching for: {query}{END}")
        for page in range(max_pages):
            start = page * results_per_page
            search_url = f"https://www.google.com/search?q={query}&start={start}&num={results_per_page}"

            try:
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                }
                response = requests.get(search_url, headers=headers)
                response.raise_for_status()

                # Extract URLs using regex
                urls = re.findall(r'href="(http[^"]+)"', response.text)

                # Filter valid URLs (exclude unwanted domains)
                valid_urls = [
                    url for url in urls
                    if url.startswith("http") and not any(exclude in url for exclude in exclude_domains)
                ]

                # Deduplicate and add new URLs
                new_urls = [url for url in valid_urls if url not in all_urls]
                if not new_urls:
                    print(f"{BLUE}Stopping search: No new results found on page {page + 1}.{END}")
                    time.sleep(delay)  # Delay between pages to avoid being blocked
                    break  # Stop search for this query if no new results are found

                all_urls.extend(new_urls)
                with open(log_file, "a") as f:
                    f.writelines(url + "\n" for url in new_urls)

                print(f"{BLUE}Page {page + 1}: {len(new_urls)} new results found.{END}")
                time.sleep(delay)  # Delay between pages to avoid being blocked

            except requests.RequestException as e:
                print(f"{RED}Failed to fetch page {page + 1}:{END}\n{e}")
                break

    return list(set(all_urls))  # Deduplicate URLs

def log_urls(urls, valid_sites, output_folder):
    """
    Logs all valid URLs to a file named `gfu.log` in the specified output folder.
    """
    filtered_urls = [url for url in urls if is_valid_file_url(url, valid_sites)]
    log_file = os.path.join(output_folder, "gfu.log")
    with open(log_file, "a") as f:
        f.writelines(url + "\n" for url in filtered_urls)
    print(f"{BLUE}Logged URLs to:{END} {log_file}")
    return filtered_urls

def list_pattern_files():
    """
    Lists all the available pattern JSON files in the pattern folder.
    """
    pattern_files = [f for f in os.listdir(PATTERN_FOLDER) if f.endswith(".json")]
    return pattern_files

def banner():
    """
    Displays the script banner.
    """
    banner = f"""
 {BLUE}\n
          ____     
   ____ _/ __/_  __
  / __ `/ /_/ / / /
 / /_/ / __/ /_/ / 
 \__, /_/  \__,_/  
/____/             \n{END}

     {BLUE}Created by{END}: @Sheryx00
     {BLUE}Github{END}: https://github.com/Sheryx00/gfu

    """
    print(banner)

def download_file(url, output_folder):
    """
    Downloads a file from the URL to the specified output folder.
    """
    try:
        response = requests.get(url, stream=True)
        file_name = os.path.join(output_folder, url.split("/")[-1])
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)
        print(f"{BLUE}Downloaded file:{END} {file_name}")

    except requests.RequestException as e:
        print(f"{RED}Failed to download file:{END} {url}\n{e}")

def load_all_patterns():
    """
    Loads all pattern JSON files from the pattern folder.
    """
    all_patterns = {}
    pattern_files = list_pattern_files()
    if not pattern_files:
        raise FileNotFoundError(f"{RED}No pattern files found in folder:{END} {PATTERN_FOLDER}")
    
    for file in pattern_files:
        pattern_name = os.path.splitext(file)[0]
        try:
            all_patterns[pattern_name] = load_pattern_file(pattern_name)
        except json.JSONDecodeError:
            print(f"{RED}Failed to load pattern file (invalid JSON):{END} {file}")
    
    return all_patterns

def main():
    banner()

    parser = argparse.ArgumentParser(description="Google Dork Search and File Downloader")
    parser.add_argument("-t", "--target", type=str, help="Target string for the search (e.g., company name)")
    parser.add_argument("-o", "--output", type=str, default="gfu", help="Output folder to save logs")
    parser.add_argument("-p", "--pattern", type=str, help="Comma-separated pattern names (e.g., api,secrets,repos)")
    parser.add_argument("-d", "--delay", type=float, default=30, help="Delay (in seconds) between search requests")
    parser.add_argument("-e", "--extension", type=str, help="Expected file extension for download (e.g., pdf, txt)")
    parser.add_argument("-x", "--extended", action="store_true", help="Download all files regardless of type")
    parser.add_argument("-l", "--list", action="store_true", help="List all available pattern JSON files")
    parser.add_argument("-a", "--aggressive", action="store_true", help="Run all patterns in the pattern folder")
    parser.add_argument("-c", "--custom", type=str, help="Custom Google dork query (e.g., 'site:{target} filetype:pdf')")

    args = parser.parse_args()

    # Handle custom query
    if args.custom:
        query = args.custom
        if "{target}" in query:
            if not args.target:
                print(f"{RED}Error: The custom query contains '{{target}}', but no target (-t) was provided.{END}")
                return
            query = query.replace("{target}", args.target)

        print(f"{BLUE}Executing custom query:{END} {query}")

        # Build a single-query list and perform the search
        queries = [query]
        urls = google_dork_search(queries, args.delay, args.output, "custom_query")
        log_urls(urls, [], args.output)

        # Optional: Download files if extensions are specified
        for url in urls:
            if args.extended or (args.extension and args.extension in url):
                download_file(url, args.output)
            elif args.extension:
                print(f"{RED}Skipping file (extension):{END} {url}")

        return

    # List pattern files if -l flag is set
    if args.list:
        files = list_pattern_files()
        if files:
            print(f"{BLUE}Available pattern files:{END}")
            for file in files:
                print(f"- {file}")
        return

    # Ensure target is specified for non-list modes
    if not args.target and not args.aggressive:
        print(f"{RED}Error: A target must be specified unless using aggressive mode.{END}")
        return

    # Ensure output folder exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Aggressive mode: process all patterns
    if args.aggressive:
        print(f"{BLUE}Aggressive mode enabled. Testing all patterns in the folder.{END}")
        try:
            all_patterns = load_all_patterns()
        except FileNotFoundError as e:
            print(e)
            return

        all_urls = []
        for pattern_name, pattern_data in all_patterns.items():
            print(f"{BLUE}Processing pattern:{END} {pattern_name}")
            queries = build_queries(pattern_data, args.target)
            valid_sites = pattern_data.get("valid_sites", [])
            urls = google_dork_search(queries, args.delay, args.output, pattern_name)
            filtered_urls = log_urls(urls, valid_sites, args.output)
            all_urls.extend(filtered_urls)

        all_urls = list(set(all_urls))  # Deduplicate across patterns
        print(f"{BLUE}Total unique URLs found:{END} {len(all_urls)}")

    # Process multiple patterns specified by -p
    elif args.pattern:
        pattern_names = args.pattern.split(",")
        all_urls = []

        for pattern_name in pattern_names:
            try:
                pattern_data = load_pattern_file(pattern_name)
            except FileNotFoundError as e:
                print(e)
                continue

            print(f"{BLUE}Processing pattern:{END} {pattern_name}")
            # Build queries and perform search
            queries = build_queries(pattern_data, args.target)
            valid_sites = pattern_data.get("valid_sites", [])
            urls = google_dork_search(queries, args.delay, args.output, pattern_name)
            filtered_urls = log_urls(urls, valid_sites, args.output)
            all_urls.extend(filtered_urls)

        # Deduplicate URLs across all patterns
        all_urls = list(set(all_urls))
        print(f"{BLUE}Total unique URLs found:{END} {len(all_urls)}")

    else:
        # Load the specific pattern
        try:
            pattern_data = load_pattern_file(args.pattern)
        except FileNotFoundError as e:
            print(e)
            return

        # Build queries and perform search
        queries = build_queries(pattern_data, args.target)
        valid_sites = pattern_data.get("valid_sites", [])
        urls = google_dork_search(queries, args.delay, args.output)
        filtered_urls = log_urls(urls, valid_sites, args.output)

    # Download files
    urls_to_download = all_urls if args.aggressive or args.pattern else filtered_urls
    for url in urls_to_download:
        if args.extended or (args.extension and args.extension in url):
            download_file(url, args.output)
        elif args.extension:
            print(f"{RED}Skipping file (extension):{END} {url}")

    if not args.extension and not args.extended:
        print(f"{BLUE}No download options specified, skipping file downloads.{END}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{RED}An unexpected error occurred:{END} {str(e)}")
