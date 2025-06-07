import json
import subprocess
import os
import config
import logging

def generate_keys():
    private_key = subprocess.check_output(["wg", "genkey"]).strip()
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key).strip()
    return private_key.decode(), public_key.decode()

def add_peer(peer_name, given_ip):
    try:
        # If IP is the same with VPN early return
        if given_ip == "10.0.0.1":
            return None, False
        
        # Generate key pair
        private_key, public_key = generate_keys()
        allowed_ips = "10.0.0.0/24"
        keepalive = 25
        
        # Add to metadata file
        peer = {"name": peer_name, "ip": given_ip, "public_key": public_key, "private_key": private_key}
        data = None
        
        try:
            with open("peers_metadata.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
        # If file doesn't exist, start fresh
            data = {"peers": []}

        # Check if IP is in use
        for current_peer in data["peers"]:
            if current_peer["ip"] == given_ip or current_peer["name"] == peer_name:
                return None, False

        data["peers"].append(peer)
        
        with open("peers_metadata.json", "w") as f:
            json.dump(data, f, indent=4)

        # Append peer to config
        with open(config.WG_CONFIG_PATH, "a") as f:
            f.write(f"#{peer_name}\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {allowed_ips}\nPersistentKeepalive = {keepalive}\n")

        # Apply new config
        subprocess.run(["sudo", "wg", "addconf", config.WG_INTERFACE, config.WG_CONFIG_PATH], check=True)

        return data, True

    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise RuntimeError("Failed to execute system command.")

    except IOError as e:
        logging.error(f"I/O error: {e}")
        raise RuntimeError("Failed to write to configuration file.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError("An unexpected error occurred.")