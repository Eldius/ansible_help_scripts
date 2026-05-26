# Project: ansible-helper-scripts

## Project Overview
A collection of Python scripts designed to assist with Ansible-related tasks. The primary tool currently provided is a host discovery script that identifies machines with open SSH ports on a given network subnet without relying on `nmap`.

### Core Technologies
- **Python**: Version >= 3.12
- **uv**: Used for project management, dependency handling, and script execution.
- **findssh**: A library used for efficient, asynchronous scanning of network ports.
- **asyncio**: Powers the non-blocking network operations.

### Architecture
- `hosts_fetch.py`: The main utility for host discovery. It calculates the subnet based on a base IP and scans it for a specified port (default 22).
- `main.py`: A placeholder entry point.
- `pyproject.toml`: Defines project metadata and dependencies.
- `Makefile`: Provides convenient shortcuts for common tasks.

## Building and Running

### Prerequisites
- Python 3.12 or higher.
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

### Key Commands
- **Scan default subnet (192.168.0.0/24)**:
  ```bash
  make hosts
  # Or directly:
  uv run python hosts_fetch.py
  ```
- **Scan specific subnet (e.g., 10.147.20.0/24)**:
  ```bash
  make hosts2
  # Or with custom base IP:
  uv run python hosts_fetch.py -b "10.147.20.1"
  ```
- **Custom Port/Timeout**:
  ```bash
  uv run python hosts_fetch.py --port 2222 --timeout 2.0
  ```

## Development Conventions

### Coding Style
- **Asynchronous Patterns**: Use `asyncio` for network-bound tasks.
- **CLI Arguments**: Follow the existing `argparse` pattern for new scripts.
- **Dependency Management**: Add new dependencies via `uv add <package>`.

### Testing
- No formal testing suite (e.g., pytest) is currently implemented. TODO: Add unit tests for subnet calculation and host filtering logic.

### Documentation
- Keep the `README.md` updated with high-level user instructions.
- Use `GEMINI.md` (this file) for AI-specific context and development-related mandates.
