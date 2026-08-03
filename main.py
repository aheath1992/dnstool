import argparse
import dns.resolver
import ipaddress
import dns.reversename

def resolve(hostname, label="internal", nameserver=None):
    records  = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
    resolver = dns.resolver.Resolver()
    if nameserver is not None:
        resolver.nameservers = [nameserver]
    results = {}
    for record in records:
        try:
            answers = resolver.resolve(hostname, record)
            results[record] = []
            for rdata in answers:
                results[record].append(rdata.to_text())
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            return f"[-] Hostname {hostname} does not exist"
    print(f"Hostname {hostname} ({label}) has the following records\n")
    for k, v in results.items():
        print(f"{k}:")
        for entry in v:
            print(f"  {entry}")
    print()

def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

def reverse_resolve(ip, label="internal", nameserver=None):
    resolver = dns.resolver.Resolver()
    if nameserver is not None:
        resolver._nameservers = [nameserver]
    rev_name = dns.reversename.from_address(ip)
    try:
        answers = resolver.resolve(rev_name, "PTR")
        print(f"Reverse lookup for {ip} ({label}):\n")
        for rdata in answers:
            print(f"  {rdata.to_text()}")
        print()
    except dns.resolver.NXDOMAIN:
        print(f"[-] No PTR record found for {ip}")
    except dns.resolver.NoAnswer:
        print(f"[-] No PTR record found for {ip}")

def main():
    parser = argparse.ArgumentParser(description="DNS lookup tool")
    parser.add_argument("hostname", help="Host or zone that you would like resolved.")
    parser.add_argument("--nameserver", default="8.8.8.8", help="External nameserver to query (default: 8.8.8.8)")
    args = parser.parse_args()
    try:
        if is_ip(args.hostname):
            reverse_resolve(ip=args.hostname, label="internal")
            reverse_resolve(ip=args.hostname, label="external", nameserver=args.nameserver)
        else:
            resolve(hostname=args.hostname, label="internal")
            resolve(hostname=args.hostname, label="external", nameserver=args.nameserver)

    except Exception as e:
        print (f"[-] Error fetching record: {e}")


if __name__ == "__main__":
    main()