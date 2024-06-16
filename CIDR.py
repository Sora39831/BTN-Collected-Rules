import ipaddress
import sys
import os
import argparse

def summarize_ip_range(ips):
    try:
        # Create a list of IPv4 addresses
        ip_list = [ipaddress.ip_address(ip) for ip in ips]
        # Create a list of summarized networks
        network_list = ipaddress.collapse_addresses(ip_list)
        return network_list
    except ValueError as e:
        print(f"Error: {e}")
        return []

def process_ip_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        ips = [line.strip() for line in infile if line.strip()]

    summarized_networks = summarize_ip_range(ips)

    with open(output_file, 'w') as outfile:
        for network in summarized_networks:
            outfile.write(f"{network}\n")

def main():
    parser = argparse.ArgumentParser(description="根据IP地址列表计算 CIDR")
    parser.add_argument('-i', '--input', required=True, help="输入ip文件路径")
    parser.add_argument('-o', '--output', required=True, help="结果文件的输出目录")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_dir = args.output
    
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: Directory '{output_dir}' not found.")
        sys.exit(1)
    
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_cidr.txt")
    
    process_ip_file(input_file, output_file)
    print(f"Processed IP addresses from {input_file} and saved results to {output_file}")

if __name__ == "__main__":
    main()
