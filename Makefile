
hosts:
	uv run ansible-hosts-fetch

hosts2:
	uv run ansible-hosts-fetch -b "10.147.20.1"

inventory:
	uv run ansible-generate-inventory -u $(USER) -b "192.168.0.1"

test:
	uv run pytest
