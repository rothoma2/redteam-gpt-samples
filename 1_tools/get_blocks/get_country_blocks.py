import requests
import os
import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2.lower()
    except LookupError:
        print(f"Invalid country name: {country_name}")
        return None

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
        return ip_blocks
    else:
        return []

if __name__ == "__main__":
    country_name = input("Enter the country name (e.g., United States, India, United Kingdom): ")
    country_code = get_country_code(country_name)

    if country_code:
        ip_blocks = get_ip_ranges(country_code)

        if ip_blocks:
            output_file = f"{country_code}.cidr"
            with open(output_file, 'w') as file:
                for ip_block in ip_blocks:
                    file.write(f"{ip_block}\n")
            print(f"IP ranges for {country_name} have been written to {output_file}.")
        else:
            print(f"Failed to retrieve IP ranges for country name {country_name}.")
    else:
        print(f"Failed to convert country name to code for {country_name}.")
