import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from ansible_help_scripts.hosts_fetch import main

def test_hosts_fetch_main(capsys):
    # Mock get_lan_ip and address2net
    with patch("ansible_help_scripts.hosts_fetch.get_lan_ip", return_value="192.168.0.5"), \
         patch("ansible_help_scripts.hosts_fetch.address2net", return_value="192.168.0.0/24"), \
         patch("ansible_help_scripts.hosts_fetch.get_hosts", new_callable=AsyncMock, return_value=[("192.168.0.10", "ssh")]):
        
        # We need to mock sys.argv if we want to test different arguments
        with patch("sys.argv", ["hosts_fetch.py", "-b", "192.168.0.1"]):
            main()
            
    captured = capsys.readouterr()
    assert "found 1 hosts" in captured.out
    assert "- 192.168.0.10: ssh" in captured.out
