import subprocess
import os
import config

def generate_keys():
    private_key = subprocess.check_output(["wg", "genkey"]).strip()
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key).strip()
    return private_key.decode(), public_key.decode()

def add_peer(peer_name):
    private_key, public_key = generate_keys()

    peer_config = f"""
# {peer_name}
[Peer]
PublicKey = {public_key}
AllowedIPs = 10.0.0.0/24
"""

    with open(config.WG_CONFIG_PATH, "a") as f:
        f.write(peer_config)

    # Apply new config
    subprocess.run(["sudo", "wg", "addconf", config.WG_INTERFACE, config.WG_CONFIG_PATH])

    # Save keys
    key_path = f"{peer_name}_private.key"
    with open(key_path, "w") as f:
        f.write(private_key + "\n")
