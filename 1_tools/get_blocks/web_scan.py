import os
import subprocess
import sys

def validate_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

def read_cidr_blocks(file_path):
    with open(file_path, 'r') as file:
        cidr_blocks = [line.strip() for line in file.readlines()]
    return cidr_blocks

def run_masscan(cidr_blocks, output_file, scan_first_block_only=False):
    if scan_first_block_only:
        cidr_blocks = cidr_blocks[:1]
    
    # Join CIDR blocks into a single string
    targets = ' '.join(cidr_blocks)
    
    # Construct the masscan command
    command = f"sudo masscan {targets} -p443 --rate=10000 -oL {output_file}"
    
    # Run the masscan command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Masscan failed with error: {stderr.decode('utf-8')}")
    else:
        print(f"Scan completed successfully. Results saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tcp_scan.py <cidr_file> [--first-block-only]")
        sys.exit(1)

    cidr_file = sys.argv[1]
    scan_first_block_only = "--first-block-only" in sys.argv

    validate_file(cidr_file)
    cidr_blocks = read_cidr_blocks(cidr_file)
    
    if not cidr_blocks:
        print(f"No CIDR blocks found in file: {cidr_file}")
        sys.exit(1)

    output_file = "masscan_results.txt"
    
    run_masscan(cidr_blocks, output_file, scan_first_block_only)
