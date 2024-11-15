#!/bin/bash
set -x
set -e

# Configure to the IP address of the container
REPL=172.12.123.10:4001
AGENT=172.12.123.11:5001

# Configure the API keys from host.env
curl -X POST -H "Content-Type: text/plain" --data-binary @host.env http://$AGENT/configure
curl http://$AGENT/status

# Configure the API keys
curl -X POST -H "Content-Type: text/plain" --data-binary @host.env http://$REPL/configure
curl http://$REPL/status

# Refresh credentials
curl -X POST http://$AGENT/refresh
curl http://$AGENT/status

# Load private data
curl -X POST http://$AGENT/load
curl http://$AGENT/status

# Save private data (not needed after refresh)
curl -X POST http://$AGENT/save
curl http://$AGENT/status

