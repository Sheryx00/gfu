# **gfu (Google File Utilizer)**

**gfu** is a Python tool for searching and downloading publicly accessible files using Google Dorks. It supports customizable search patterns, aggressive search mode, random user-agent rotation, and advanced logging and filtering capabilities.

## Features

- Perform Google Dork searches using custom JSON pattern files.
- Test multiple patterns or combine them with the `-p` option.
- Aggressive mode to use all patterns from the `.gfu` folder automatically.
- Randomized User-Agent for each request to reduce detection risk.
- Log all discovered URLs to `gfu.log`.
- Optional file downloading with flexible filtering by file extension.

## Installation

Clone this repository:

```bash
git clone https://github.com/sheryx00/gfu.git
```

## Usage

### List All Available Patterns

```bash
python3 gfu.py -l
```
### Search with a Single Pattern

```bash
python3 gfu.py -t "example.com" -p api -o ./results --delay 2
```

### Combine Multiple Patterns

```bash
python3 gfu.py -t "example.com" -p api,secrets,repos -o ./results --delay 3
```

### Aggressive Mode

```bash
python3 gfu.py -t "example.com" -a -o ./results --delay 2
```

### Filter Downloads by File Extension

```bash
python3 gfu.py -t "example.com" -p api -o ./results --extension pdf
```

# Download All File Types

```bash
python3 gfu.py -t "example.com" -p secrets -o ./results --extended
```
## Help

```bash
-t, --target	    Target string for the search (e.g., domain name).
-o, --output	    Output folder to save logs and downloaded files. (Required)
-p, --pattern	    Comma-separated list of pattern names (e.g., api,secrets,repos).
-a, --aggressive	Enable aggressive mode to use all patterns in the .gfu folder.
-d, --delay	        Delay (in seconds) between requests. Default is 2.0.
-e, --extension	    Filter downloads by specific file extension (e.g., pdf, txt, csv).
-x, --extended	    Download all files regardless of extension.
-l, --list	        List all available pattern JSON files.
```

## Support

Support the creator to keep sharing new tools: <a href="https://www.buymeacoffee.com/Sheryx00" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
