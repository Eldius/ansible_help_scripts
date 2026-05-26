
hosts:
	uv run python hosts_fetch.py

hosts2:
	uv run python hosts_fetch.py -b "10.147.20.1"

inventory:
	uv run python generate_inventory.py -u $(USER) -b "192.168.0.1"

test:
	uv run pytest
