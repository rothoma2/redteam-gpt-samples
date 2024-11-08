import requests
import os

def download_country_ip_blocks(country_code):
    base_url = "https://raw.githubusercontent.com/herrbischoff/country-ip-blocks/master/ipv4"
    file_url = f"{base_url}/{country_code}.cidr"
    print(file_url)

    response = requests.get(file_url)
    if response.status_code == 200:
        file_path = f"{country_code}.cidr"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        print(f"Failed to download file for country code {country_code}: {response.status_code}")
        return None

def parse_ip_blocks(file_path):
    with open(file_path, 'r') as file:
        ip_blocks = [line.strip() for line in file.readlines()]
    return ip_blocks

def get_ip_ranges(country_code):
    file_path = download_country_ip_blocks(country_code)
    if file_path:
        ip_blocks = parse_ip_blocks(file_path)
        os.remove(file_path)
        return ip_blocks
    else:
        return []

if __name__ == "__main__":
    country_code = "cr"  # Replace with the desired country code
    ip_blocks = get_ip_ranges(country_code)

    if ip_blocks:
        print(f"IP Ranges for {country_code}:")
        for ip_block in ip_blocks:
            print(ip_block)
    else:
        print(f"Failed to retrieve IP ranges for country code {country_code}.")