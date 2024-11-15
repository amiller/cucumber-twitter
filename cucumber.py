from flask import Flask, jsonify, request
import subprocess
import requests
import sys
import os
import time
from eth_keys import keys
import psutil

app = Flask(__name__)

SECURE_FILE = os.environ['SECURE_FILE']

# Process a .env file
def load_dotenv(data):
    env_data = data.decode('utf-8')
    config = {}
    for line in env_data.splitlines():
        line = line.strip()
        if line.startswith('#'): continue
        if not '=' in line: continue
        key, value = line.split('=', 1)
        config[key.strip()] = value.strip()
    return config

# Pass API keys and other arguments from the host
@app.route('/configure', methods=['POST'])
def configure():
    config = load_dotenv(request.data)

    print('Received configuration parameters:', config.keys(),
          file=sys.stderr)
    os.environ['ETH_RPC_URL'] = config['ETH_RPC_URL']
    os.environ['X_AUTH_TOKENS'] = config['X_AUTH_TOKENS']    
    os.environ['X_PASSWORD'] = config['X_PASSWORD']
    os.environ['X_EMAIL'] = config['X_EMAIL']
    os.environ['PROTONMAIL_PASSWORD'] = config['PROTONMAIL_PASSWORD']
    os.environ['AGENT_WALLET_PRIVATE_KEY'] = config['AGENT_WALLET_PRIVATE_KEY']
    return "Configuration OK", 200

# Called by untrusted host to refresh the auth credentials
@app.route('/refresh', methods=['POST'])
def refresh():
    result = subprocess.check_output("python3 scripts/login_get_cookie.py", shell=True, stderr=sys.stderr, env=os.environ.copy())
    config = load_dotenv(open('cookies.env','rb').read())
    os.environ['X_AUTH_TOKENS'] = config['X_AUTH_TOKENS']    
    print(config, file=sys.stderr)
    return "OK", 200

# Called by untrusted host to store the credentials
@app.route('/save', methods=['POST'])
def save():
    # May be called by host
    ip_address = request.remote_addr

    with open(SECURE_FILE,'w') as f:
        for k in ['X_AUTH_TOKENS',
                  'X_PASSWORD',
                  'PROTONMAIL_PASSWORD',
                  'AGENT_WALLET_PRIVATE_KEY']:
            f.write(f"{k}={os.environ[k]}\n")
    return "Wrote save file", 200

# Called by untrusted host to store the credentials
@app.route('/load', methods=['POST'])
def load():
    # May be called by host
    ip_address = request.remote_addr
    config = load_dotenv(open(SECURE_FILE,'rb').read())
    os.environ['X_AUTH_TOKENS'] = config['X_AUTH_TOKENS'].replace('\\"','"')
    os.environ['X_PASSWORD'] = config['X_PASSWORD']
    os.environ['PROTONMAIL_PASSWORD'] = config['PROTONMAIL_PASSWORD']
    os.environ['AGENT_WALLET_PRIVATE_KEY'] = config['AGENT_WALLET_PRIVATE_KEY']
    return "Loaded save file", 200

@app.route('/timeline', methods=['GET'])
def timeline():
    ip_address = request.remote_addr
    return "OK", 200

@app.route('/status', methods=['GET'])
def status():
    ip_address = request.remote_addr
    return ip_address, 200

@app.route('/encumber', methods=['POST'])
def encumber():
    ip_address = request.remote_addr
    X_PASSWORD = subprocess.check_output("python3 scripts/twitter.py", shell=True, env=os.environ.copy()).decode('utf-8').strip()
    print(X_PASSWORD, file=sys.stderr)
    os.environ['X_PASSWORD'] = X_PASSWORD
    save()
    return "Encumbered account", 200

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

if __name__ == '__main__':
    time.sleep(1)
    port = 5001
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
