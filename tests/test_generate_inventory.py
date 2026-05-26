import asyncio
import os
import yaml
import pytest
import asyncssh
from ipaddress import IPv4Address
from unittest.mock import AsyncMock, patch, MagicMock
from ansible_help_scripts.generate_inventory import get_hostname, generate_inventory

@pytest.mark.asyncio
async def test_get_hostname_success():
    mock_result = MagicMock()
    mock_result.stdout = "test-host\n"
    
    mock_conn = AsyncMock()
    mock_conn.run.return_value = mock_result
    mock_conn.__aenter__.return_value = mock_conn
    
    with patch("asyncssh.connect", return_value=mock_conn):
        host, hostname = await get_hostname("1.2.3.4", 22, "user")
        assert host == "1.2.3.4"
        assert hostname == "test-host"

@pytest.mark.asyncio
async def test_get_hostname_permission_denied():
    # PermissionDenied is usually raised when connecting or authenticating
    # If it happens during 'async with', it means it was raised by connect() or __aenter__
    with patch("asyncssh.connect", side_effect=asyncssh.PermissionDenied("Auth failed")):
        host, hostname = await get_hostname("1.2.3.4", 22, "user")
        assert host == "1.2.3.4"
        assert hostname is None

@pytest.mark.asyncio
async def test_get_hostname_other_error():
    with patch("asyncssh.connect", side_effect=OSError("Network down")):
        host, hostname = await get_hostname("1.2.3.4", 22, "user")
        assert host == "1.2.3.4"
        assert hostname is None

@pytest.mark.asyncio
async def test_generate_inventory_full_flow(tmp_path):
    output_file = tmp_path / "test_inventory.yaml"
    
    # Mock hosts discovery
    mock_discovered = [(IPv4Address("192.168.0.10"), "ssh"), (IPv4Address("192.168.0.20"), "ssh")]
    
    # Mock hostname retrieval
    async def mock_get_hostname(host, *args, **kwargs):
        if host == "192.168.0.10":
            return host, "host10"
        return host, None

    with patch("ansible_help_scripts.generate_inventory.get_hosts", AsyncMock(return_value=mock_discovered)), \
         patch("ansible_help_scripts.generate_inventory.get_hostname", side_effect=mock_get_hostname):
        
        await generate_inventory(
            baseip="192.168.0.1",
            port=22,
            timeout=1.0,
            user="user",
            output_file=str(output_file)
        )
    
    assert output_file.exists()
    with open(output_file) as f:
        data = yaml.safe_load(f)
        
    assert "all" in data
    assert "hosts" in data["all"]
    assert "host10" in data["all"]["hosts"]
    assert data["all"]["hosts"]["host10"]["ansible_host"] == "192.168.0.10"
    assert "192.168.0.20" in data["all"]["hosts"]
    assert data["all"]["hosts"]["192.168.0.20"]["ansible_host"] == "192.168.0.20"
