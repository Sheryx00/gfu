# **gfu (Google-Fu)**

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
:scroll: Check [gfu-patterns](https://github.com/Sheryx00/gfu-patterns) to download my patterns list. (rememeber to copy them inside the ~/.gfu folder)

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
Google Dork Search and File Downloader

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target string for the search (e.g., domain.com)
  -f FILE, --file FILE  File containing a list of targets (one per line)
  -o OUTPUT, --output OUTPUT
                        Output folder to save logs
  -p PATTERN, --pattern PATTERN
                        Comma-separated pattern names (e.g., api,secrets,repos)
  -d DELAY, --delay DELAY
                        Delay (in seconds or range) between search requests
  -e EXTENSION, --extension EXTENSION
                        Expected file extension for download (e.g., pdf, txt)
  -x, --extended        Download all files regardless of type
  -l, --list            List all available pattern JSON files
  -a, --aggressive      Run all patterns in the pattern folder
  -c CUSTOM, --custom CUSTOM
                        Custom Google dork query (e.g., 'site:{target} filetype:pdf')
```

## Support

Support the creator to keep sharing new tools:
<a href="https://www.buymeacoffee.com/Sheryx00" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
