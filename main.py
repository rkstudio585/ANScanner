import subprocess
import socket
import logging
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import box
from pyfiglet import figlet_format
import threading

# Setup logging
logging.basicConfig(filename='scan.log', level=logging.INFO)

# Initialize console for rich output
console = Console()
scan_results = []

def print_banner():
    """Print the ASCII banner using pyfiglet."""
    banner = figlet_format("ANScanner", font="slant")
    console.print(banner, style="bold cyan")

def resolve_ip_range(input_range):
    """Resolve the input to get a list of IP addresses or return an IP range."""
    input_range = input_range.split(':')[0]  # Strip the port if present
    try:
        ip_address = socket.gethostbyname(input_range)
        return [ip_address]  # Return a list with the resolved IP address
    except socket.gaierror:
        # Handle the case where input is not a valid domain
        console.print("[red]Invalid domain name. Scanning local IP range instead...[/red]")
        return [f"{input_range}.{i}" for i in range(1, 255)]  # /24 subnet

def scan_network(ip_range):
    """Scan the specified IP range for active hosts using Nmap."""
    try:
        command = ["nmap", "-sn", ip_range]  # Ping scan
        output = subprocess.check_output(command, universal_newlines=True)  # Get the output
        return parse_nmap_output(output)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error during Nmap scan: {e}[/red]")
        return []
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        return []

def parse_nmap_output(output):
    """Parse the output of the Nmap command to extract live hosts."""
    active_hosts = []
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            host = line.split(" ")[-1]  # Extract the IP address
            active_hosts.append(host)
    return active_hosts

def port_scan(ip_address):
    """Scan common ports on the given IP address using Nmap and return open ports."""
    try:
        command = ["nmap", "-p", "1-1024", ip_address]  # Scan common ports (1-1024)
        output = subprocess.check_output(command, universal_newlines=True)  # Get the output
        return parse_port_output(output)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error scanning {ip_address}: {e}[/red]")
        return []
    except Exception as e:
        console.print(f"[red]An unexpected error occurred while scanning {ip_address}: {e}[/red]")
        return []

def parse_port_output(output):
    """Parse the output of the Nmap port scan to extract open ports."""
    open_ports = []
    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            parts = line.split()
            port = parts[0].split("/")[0]  # Extract the port number
            service = parts[2] if len(parts) > 2 else "unknown"
            open_ports.append(f"{port} ({service})")
    return open_ports

def os_detection(ip_address):
    """Detect the operating system of the host."""
    try:
        command = ["nmap", "-O", ip_address]  # OS detection
        output = subprocess.check_output(command, universal_newlines=True)  # Get the output
        return parse_os_output(output)
    except subprocess.CalledProcessError:
        return "Unknown OS"
    except Exception as e:
        return f"Error detecting OS: {e}"

def parse_os_output(output):
    """Parse the output to find the OS."""
    for line in output.splitlines():
        if "OS details" in line:
            return line.split(":")[-1].strip()
    return "Unknown OS"

def display_results(active_hosts):
    """Display the scan results in a styled table."""
    table = Table(title="Active Hosts", box=box.SIMPLE)
    table.add_column("IP Address", justify="center", style="cyan")
    table.add_column("Open Ports", justify="center", style="magenta")
    table.add_column("Operating System", justify="center", style="green")

    for host in active_hosts:
        open_ports = port_scan(host)
        os_info = os_detection(host)
        table.add_row(host, ", ".join(open_ports) if open_ports else "None", os_info)

    console.print(table)

def scan_worker(ip_range):
    """Thread worker to scan network."""
    active_hosts = scan_network(ip_range)
    return active_hosts

def main():
    print_banner()
    input_range = console.input("[white]Enter the IP range or domain (e.g., IP or example.com): [/white]")
    
    console.print("[yellow]Scanning... Please wait...[/yellow]")
    ip_range = resolve_ip_range(input_range)

    active_hosts = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=len(ip_range))
        
        for ip in ip_range:
            active_hosts.extend(scan_worker(ip))
            progress.update(task, advance=1)

    if active_hosts:
        console.print(f"[green]Active hosts found: {len(active_hosts)}[/green]")
        display_results(active_hosts)
    else:
        console.print("[red]No active hosts found.[/red]")

if __name__ == "__main__":
    main()
      
