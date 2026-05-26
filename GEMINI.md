# Project: ansible-helper-scripts

## Project Overview
A collection of Python scripts designed to assist with Ansible-related tasks. The primary tool currently provided is a host discovery script that identifies machines with open SSH ports on a given network subnet without relying on `nmap`.

### Core Technologies
- **Python**: Version >= 3.12
- **uv**: Used for project management, dependency handling, and script execution.
- **findssh**: A library used for efficient, asynchronous scanning of network ports.
- **asyncio**: Powers the non-blocking network operations.

### Architecture
- `src/ansible_helper_scripts/`: The main package directory.
  - `hosts_fetch.py`: The utility for host discovery.
  - `generate_inventory.py`: Generates an Ansible inventory YAML file.
  - `main.py`: Entry point.
- `pyproject.toml`: Defines project metadata, dependencies, and CLI entry points.
- `Makefile`: Provides convenient shortcuts for common tasks.

## Building and Running

### Prerequisites
- Python 3.12 or higher.
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

### Key Commands
- **Scan default subnet (192.168.0.0/24)**:
  ```bash
  make hosts
  # Or via CLI:
  uv run ansible-hosts-fetch
  ```
- **Generate Ansible Inventory**:
  ```bash
  # Using Makefile (defaults to current user and 192.168.0.1)
  make inventory
  
  # Using CLI for custom settings
  uv run ansible-generate-inventory -u myuser -b "10.0.0.1" -k ~/.ssh/id_rsa -o my_inventory.yaml
  ```
- **Scan specific subnet (e.g., 10.147.20.0/24)**:
  ```bash
  make hosts2
  # Or via CLI:
  uv run ansible-hosts-fetch -b "10.147.20.1"
  ```
- **Custom Port/Timeout**:
  ```bash
  uv run ansible-hosts-fetch --port 2222 --timeout 2.0
  ```

## Development Conventions

### Coding Style
- **Asynchronous Patterns**: Use `asyncio` for network-bound tasks.
- **CLI Arguments**: Follow the existing `argparse` pattern for new scripts.
- **Dependency Management**: Add new dependencies via `uv add <package>`.

### Testing
- Comprehensive test suite implemented using `pytest` and `pytest-asyncio`, covering host discovery, SSH connectivity, and inventory generation.

### Documentation
- Keep the `README.md` updated with high-level user instructions.
- Use `GEMINI.md` (this file) for AI-specific context and development-related mandates.

## Testing

### Running Tests
The project uses `pytest` and `pytest-asyncio` for testing.
```bash
make test
# Or directly:
PYTHONPATH=. uv run pytest
```

### Testing Strategy
- **Mocks**: Network operations and SSH connections are mocked using `unittest.mock`.
- **Asyncio**: `pytest-asyncio` is used to test asynchronous functions.
- **Inventory Validation**: Tests verify that the generated YAML structure is correct for Ansible.
