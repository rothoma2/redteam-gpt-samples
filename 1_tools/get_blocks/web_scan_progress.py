import os
import subprocess
import sys
import ipaddress
import time
from rich.progress import Progress
from rich.console import Console

console = Console()

def validate_file(file_path):
    if not os.path.isfile(file_path):
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        sys.exit(1)

def read_cidr_blocks(file_path):
    with open(file_path, 'r') as file:
        cidr_blocks = [line.strip() for line in file.readlines()]
    return cidr_blocks

def translate_to_24_blocks(cidr_blocks):
    subnets_24 = []
    for block in cidr_blocks:
        network = ipaddress.ip_network(block)
        if network.prefixlen <= 24:
            subnets_24.extend(str(subnet) for subnet in network.subnets(new_prefix=24))
        else:
            subnets_24.append(str(network))
    return subnets_24

def run_masscan(cidr_block, output_file):
    # Construct the masscan command
    command = f"sudo masscan {cidr_block} -p443 --rate=10000 -oL {output_file}"
    
    # Run the masscan command and measure the time
    start_time = time.time()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    end_time = time.time()
    
    scan_time = end_time - start_time
    
    if process.returncode != 0:
        console.print(f"[bold red]Masscan failed for {cidr_block} with error: {stderr.decode('utf-8')}[/bold red]")
        return None
    else:
        console.print(f"[green]Scan for {cidr_block} completed successfully in {scan_time:.2f} seconds.[/green]")
        # Read and print the results
        with open(output_file, 'r') as result_file:
            results = result_file.read()
            console.print(f"[blue]Results for {cidr_block}:\n{results}[/blue]")
        return scan_time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: python tcp_scan.py <cidr_file> [--first-block-only][/bold red]")
        sys.exit(1)

    cidr_file = sys.argv[1]
    scan_first_block_only = "--first-block-only" in sys.argv

    validate_file(cidr_file)
    cidr_blocks = read_cidr_blocks(cidr_file)
    
    if not cidr_blocks:
        console.print(f"[bold red]No CIDR blocks found in file: {cidr_file}[/bold red]")
        sys.exit(1)

    subnets_24 = translate_to_24_blocks(cidr_blocks)
    if scan_first_block_only:
        subnets_24 = subnets_24[:1]

    results_file = "masscan_results.txt"
    with open(results_file, 'a') as file, Progress() as progress:
        task = progress.add_task("[cyan]Scanning[/cyan]", total=len(subnets_24))
        for subnet in subnets_24:
            scan_time = run_masscan(subnet, f"masscan_{subnet.replace('/', '_')}.txt")
            if scan_time is not None:
                file.write(f"{subnet} - {scan_time:.2f} seconds\n")
            progress.update(task, advance=1)
