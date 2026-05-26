import asyncio
import yaml
from argparse import ArgumentParser
from ipaddress import IPv4Address
from typing import Dict, List, Tuple

import asyncssh
from findssh import get_hosts, get_lan_ip, address2net

DEFAULT_PORT = 22
DEFAULT_TIMEOUT = 1.0
DEFAULT_BASEIP = "192.168.0.1"
DEFAULT_OUTPUT = "inventory.yaml"

async def get_hostname(host: str, port: int, user: str, password: str = None, client_keys: List[str] = None) -> Tuple[str, str]:
    """Connect to host via SSH and run 'hostname' command."""
    try:
        async with asyncssh.connect(
            host,
            port=port,
            username=user,
            password=password,
            client_keys=client_keys,
            known_hosts=None,  # Skip host key verification for discovery
        ) as conn:
            result = await conn.run("hostname", check=True)
            hostname = result.stdout.strip()
            return host, hostname
    except asyncssh.PermissionDenied:
        # Ignore permission errors as requested
        return host, None
    except (asyncssh.Error, OSError) as e:
        print(f"Failed to connect to {host}: {e}")
        return host, None

async def generate_inventory(
    baseip: str,
    port: int,
    timeout: float,
    user: str,
    password: str = None,
    key_path: str = None,
    output_file: str = DEFAULT_OUTPUT,
):
    """Scan subnet, fetch hostnames, and save Ansible inventory."""
    net = address2net(IPv4Address(baseip))
    print(f"Scanning network: {net}...")

    # Step 1: Discover hosts with open SSH port
    discovered = await get_hosts(net, port, timeout)
    if not discovered:
        print("No hosts found.")
        return

    print(f"Found {len(discovered)} hosts. Fetching hostnames...")

    # Step 2: Concurrently fetch hostnames
    client_keys = [key_path] if key_path else None
    tasks = [
        get_hostname(str(host), port, user, password, client_keys)
        for host, _ in discovered
    ]
    results = await asyncio.gather(*tasks)

    # Step 3: Build Ansible inventory structure
    inventory = {
        "all": {
            "hosts": {}
        }
    }

    for ip, hostname in results:
        # Use hostname as key if available, otherwise fallback to IP
        name = hostname if hostname else ip
        inventory["all"]["hosts"][name] = {
            "ansible_host": ip
        }

    # Step 4: Save to YAML
    with open(output_file, "w") as f:
        yaml.dump(inventory, f, default_flow_style=False)

    print(f"Inventory saved to {output_file}")

def main():
    p = ArgumentParser(description="Generate Ansible inventory by scanning network and fetching hostnames via SSH.")
    p.add_argument("-b", "--baseip", default=DEFAULT_BASEIP, help="Subnet base IP to scan")
    p.add_argument("-u", "--user", required=True, help="SSH username")
    p.add_argument("-p", "--password", help="SSH password")
    p.add_argument("-k", "--key", help="Path to SSH private key")
    p.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output YAML file")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help="SSH port")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Scan timeout")

    args = p.parse_args()

    asyncio.run(
        generate_inventory(
            args.baseip,
            args.port,
            args.timeout,
            args.user,
            args.password,
            args.key,
            args.output,
        )
    )

if __name__ == "__main__":
    main()
