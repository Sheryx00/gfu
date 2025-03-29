'''googlesearch is a Python library for searching Google, easily.

This is a fork of the original googlesearch proyect:
https://github.com/Nv7-GitHub/googlesearch

We thanks to googlesearch's collaborators for sharing this!
'''
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote # to decode the url
from user_agents import get_useragent


def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify, region):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent(),
            "Accept": "*/*"
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
            "safe": safe,
            "gl": region,
        },
        proxies=proxies,
        timeout=timeout,
        verify=ssl_verify,
        cookies = {
            'CONSENT': 'PENDING+987', # Bypasses the consent page
            'SOCS': 'CAESHAgBEhIaAB',
        }
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, safe="active", ssl_verify=None, region=None, start_num=0, unique=False):
    """Search the Google search engine"""

    # Proxy setup
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http") or proxy.startswith("socks5")) else None

    start = start_num
    fetched_results = 0  # Keep track of the total fetched results
    fetched_links = set() # to keep track of links that are already seen previously

    while fetched_results < num_results:
        sleep(sleep_interval) # be patient
        resp = _req(term, num_results - start, lang, start, proxies, timeout, safe, ssl_verify, region)
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", class_="ezO2md")

        if not result_block:  # If no results are found at all, stop looping
            print("No more results found.")
            break

        new_results = 0  

        for result in result_block:
            link_tag = result.find("a", href=True)
            title_tag = link_tag.find("span", class_="CVA68e") if link_tag else None
            description_tag = result.find("span", class_="FrIlee")

            if link_tag and title_tag and description_tag:
                link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", ""))
                
                if link in fetched_links and unique:
                    continue  

                fetched_links.add(link)
                title = title_tag.text
                description = description_tag.text
                fetched_results += 1
                new_results += 1

                if advanced:
                    yield SearchResult(link, title, description)
                else:
                    yield link

                if fetched_results >= num_results:
                    return  # Instead of `break`, `return` stops the generator entirely

        if new_results == 0:  
            print(f"{fetched_results} results found. Stopping search.")
            break  

        start += 10