# /// script
# requires-python = ">=3.12"
# ///

import asyncio
from argparse import ArgumentParser
from ipaddress import IPv4Address

from findssh import get_hosts,get_lan_ip,address2net

PORT = 22
TIMEOUT = 1.0
BASEIP = "192.168.0.1"

def main():
    p = ArgumentParser("scan for hosts with open port, without NMAP")
    p.add_argument("-p", "--port", help="single port to try", default=PORT, type=int)
    p.add_argument(
        "-s", "--service", default="", help="string to match to qualify detections"
    )
    p.add_argument(
        "-t",
        "--timeout",
        help="timeout to wait for server. Must be finite or will hang.",
        type=float,
        default=TIMEOUT,
    )
    p.add_argument("-b", "--baseip", default=BASEIP, help="set a specific subnet to scan")
    args = p.parse_args()

    own_ip = get_lan_ip()
    print("own address", own_ip)
    net = address2net(IPv4Address(args.baseip))
    print("searching", net)

    result = asyncio.run(get_hosts(net, args.port, args.timeout, args.service))

    print(
        f"\n\n---\nfound {len(result)} hosts with open port {args.port} on {args.baseip} subnet"
    )
    for host, service in result:
        print(f"- {host}: {service}")


if __name__ == "__main__":
    main()
