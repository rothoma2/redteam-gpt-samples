import os
import sys
import ipaddress

def validate_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
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

def write_to_file(subnets_24, output_file):
    with open(output_file, 'w') as file:
        for subnet in subnets_24:
            file.write(f"{subnet}\n")
    print(f"Translated subnets written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate_cidr.py <cidr_file>")
        sys.exit(1)

    cidr_file = sys.argv[1]
    output_file = "translated_subnets.txt"

    validate_file(cidr_file)
    cidr_blocks = read_cidr_blocks(cidr_file)
    
    if not cidr_blocks:
        print(f"No CIDR blocks found in file: {cidr_file}")
        sys.exit(1)

    subnets_24 = translate_to_24_blocks(cidr_blocks)
    write_to_file(subnets_24, output_file)
