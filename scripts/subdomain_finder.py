import requests
from rich.console import Console

console = Console()

def fetch_subdomains(domain):
    """
    Uses crt.sh public API to find subdomains of a given domain.
    """
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        console.print(f"[bold cyan]Fetching subdomains for:[/bold cyan] {domain}")
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            console.print(f"[red]Error:[/red] Received {response.status_code}")
            return []
        data = response.json()
        subdomains = sorted({entry["name_value"] for entry in data})
        return subdomains
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return []

def save_to_file(subdomains, domain):
    """Save results to outputs/ folder."""
    output_path = f"outputs/{domain}_subdomains.txt"
    with open(output_path, "w") as f:
        for sub in subdomains:
            f.write(sub + "\n")
    console.print(f"[green]Saved {len(subdomains)} subdomains → {output_path}[/green]")

if __name__ == "__main__":
    target = input("Enter target domain (e.g. example.com): ").strip()
    subs = fetch_subdomains(target)
    if subs:
        save_to_file(subs, target)
