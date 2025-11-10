#!/usr/bin/env python3
"""
Enhanced Subdomain Finder
Usage:
  python scripts/subdomain_finder.py -d example.com -o outputs/
"""

import argparse
import requests
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

def fetch_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    console.print(f"[bold cyan]Fetching subdomains for:[/bold cyan] {domain}")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            console.print(f"[red]HTTP error {response.status_code}[/red]")
            return []
        data = response.json()
        subs = sorted({entry["name_value"] for entry in data if "name_value" in entry})
        return subs
    except Exception as e:
        console.print(f"[red]Error fetching data:[/red] {e}")
        return []

def save_to_file(subdomains, output_dir, domain):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{domain}_subdomains_{datetime.now():%Y%m%d%H%M%S}.txt")
    with open(filename, "w") as f:
        for sub in subdomains:
            f.write(sub + "\n")
    console.print(f"[green]Saved {len(subdomains)} subdomains → {filename}[/green]")

def main():
    parser = argparse.ArgumentParser(description="Find subdomains using crt.sh")
    parser.add_argument("-d", "--domain", required=True, help="Target domain, e.g. example.com")
    parser.add_argument("-o", "--output", default="outputs", help="Output directory")
    args = parser.parse_args()

    subs = fetch_subdomains(args.domain)
    if subs:
        save_to_file(subs, args.output, args.domain)
    else:
        console.print("[yellow]No subdomains found.[/yellow]")

if __name__ == "__main__":
    main()
