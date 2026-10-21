# Torrent Peer IP Collector

A small Python utility that connects to the qBittorrent Web API, checks the torrents managed by the configured qBittorrent instance, and saves the peer IP addresses returned by the API as JSON files.

> **Privacy and responsible use:** IP addresses can be sensitive information. Use this tool only on a qBittorrent instance and network you are authorized to monitor. Do not use collected data to identify, target, harass, or expose other people, and do not publish the collected IP lists.

## Features

- Authenticates with the qBittorrent Web API.
- Retrieves the torrents currently known to the configured qBittorrent instance.
- Queries peer information for each torrent and extracts available `ip` fields.
- Deduplicates IP addresses with a Python `set`.
- Stores the collected addresses as numbered JSON files.
- Reads configuration from environment variables or a local `.env` file.

## Requirements

- Python 3.8 or newer
- qBittorrent with the Web UI enabled
- An account authorized to access that Web UI
- The `requests` and `python-dotenv` Python packages

## Installation

1. Clone or download this repository and open a terminal in the project directory.
2. Install the dependencies:

   ```bash
   python -m pip install requests python-dotenv
   ```

3. Create a `.env` file in the project directory:

   ```dotenv
   QB_URL=http://127.0.0.1:8080
   QB_USERNAME=your_qbittorrent_username
   QB_PASSWORD=your_qbittorrent_password
   OUTPUT_DIR=scraped_ips
   IP_LIMIT=100
   ```

   Replace the URL and credentials with those for your own qBittorrent Web UI. `QB_URL` should be the base URL, without a trailing slash. The example assumes the Web UI is available on the same machine at port `8080`.

   **Keep `.env` private.** Do not commit passwords or other credentials to source control. Consider adding `.env` and the output directory to `.gitignore`.

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `QB_URL` | Yes | — | Base URL of the qBittorrent Web UI, for example `http://127.0.0.1:8080` |
| `QB_USERNAME` | Yes | — | qBittorrent Web UI username |
| `QB_PASSWORD` | Yes | — | qBittorrent Web UI password |
| `OUTPUT_DIR` | No | `scraped_ips` | Directory where JSON output files are saved |
| `IP_LIMIT` | No | `100` | Maximum number of IP addresses written to each JSON file; must be a positive integer |

## Usage

Run the script Python App.py

```bash
python App.py
```

The program logs in, retrieves the current torrent list, collects the peer IP addresses exposed by the API, and saves any results. It then repeats this process continuously. Press **Ctrl+C** to stop it.

## Output

The output directory is created automatically when there are IP addresses to save. The files are named `ips_1.json`, `ips_2.json`, and so on. Each file contains a JSON array of up to `IP_LIMIT` unique IP address strings.

Example:

```json
[
    "192.0.2.10",
    "2001:db8::10"
]
```

The addresses above are documentation examples, not collected data. The script stores unique IP addresses across runs; it does not preserve which torrent or peer each address came from, timestamps, or other peer metadata.

## How it works

1. `login()` authenticates using the credentials configured in the environment.
2. `get_torrents()` requests the torrent list.
3. `get_peers()` requests peer information for each torrent hash and extracts peer IP addresses.
4. `load_ips()` reads existing JSON files to build a set of previously collected addresses.
5. `save_ips()` merges newly observed addresses with the existing set and writes the result into numbered JSON chunks.

## Limitations and operational notes

- This is an **API-based data collector**, not an HTML/DOM web scraper.
- The current implementation has no delay between polling cycles. It can repeatedly call the API as quickly as possible; add a configurable sleep interval before running it for extended periods.
- Requests do not currently specify timeouts, and network or JSON errors are not handled with retries/backoff. A failed request may stop the script or leave it waiting indefinitely.
- `IP_LIMIT` must be greater than zero.
- Output order is not guaranteed because addresses are stored in a set.
- Only peer IP addresses returned by the qBittorrent API are collected; results depend on the torrents and peer information visible to the configured client.

## Security

- Prefer keeping the qBittorrent Web UI bound to localhost or a trusted private network; do not expose it publicly just to run this script.
- Keep credentials in environment variables or a protected `.env` file.
- Treat the output as potentially sensitive data, restrict access to it, and remove it when it is no longer needed.

## License

No license is specified here. Add a `LICENSE` file if you intend to define how others may use, modify, or redistribute this project.
