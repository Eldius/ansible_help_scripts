# Ansible Helper Scripts

A collection of lightweight, high-performance Python utilities for Ansible host discovery and inventory management.

## Features

- **Fast Host Discovery**: Identify active SSH servers on a subnet without requiring `nmap`.
- **Automated Inventory Generation**: Scan your network and automatically build an Ansible YAML inventory by querying hostnames via SSH.
- **Asynchronous & Concurrent**: Built with `asyncio` and `asyncssh` for high-speed network operations.
- **Modern Python**: Fully compatible with Python 3.12+ and managed with `uv`.

## Installation

This project uses `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/youruser/ansible-helper-scripts.git
cd ansible-helper-scripts

# Sync dependencies and create virtual environment
uv sync
```

## CLI Usage

The package provides two main CLI tools:

### 1. Host Discovery (`ansible-hosts-fetch`)
Scans a subnet to find active SSH servers (default port 22).

```bash
# Scan default subnet (192.168.0.0/24)
uv run ansible-hosts-fetch

# Scan specific base IP
uv run ansible-hosts-fetch -b 10.0.0.1
```

### 2. Inventory Generator (`ansible-generate-inventory`)
Scans the network, retrieves hostnames via SSH, and outputs a `inventory.yaml`.

```bash
# Generate inventory using current user and default subnet
uv run ansible-generate-inventory -u $(whoami)

# Full options
uv run ansible-generate-inventory -u myuser -b 10.0.0.1 -k ~/.ssh/id_rsa -o prod_inventory.yaml
```

## Using as a Python Module

You can also import and use the discovery or inventory logic in your own Python scripts.

### Import Discovery Logic
```python
import asyncio
from ansible_helper_scripts.hosts_fetch import get_hosts
from ipaddress import IPv4Network

async def find_my_servers():
    network = IPv4Network("192.168.1.0/24")
    hosts = await get_hosts(network, port=22, timeout=1.0)
    for host, service in hosts:
        print(f"Found {host}")

asyncio.run(find_my_servers())
```

### Import Inventory Logic
```python
import asyncio
from ansible_helper_scripts.generate_inventory import generate_inventory

async def build_inventory():
    await generate_inventory(
        baseip="192.168.0.1",
        port=22,
        timeout=1.0,
        user="admin",
        output_file="dynamic_inventory.yaml"
    )

asyncio.run(build_inventory())
```

## Development

### Running Tests
```bash
make test
# or
uv run pytest
```

### Project Structure
- `src/ansible_helper_scripts/`: Core logic and CLI entry points.
- `tests/`: Comprehensive test suite with mocked network operations.
- `Makefile`: Shortcuts for common tasks.
