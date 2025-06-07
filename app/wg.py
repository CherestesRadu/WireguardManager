import subprocess
import os
import config
import logging

def generate_keys():
    private_key = subprocess.check_output(["wg", "genkey"]).strip()
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key).strip()
    return private_key.decode(), public_key.decode()

def add_peer(peer_name):
    try:
        # Generate key pair
        private_key, public_key = generate_keys()
        allowed_ips = "10.0.0.0/24"
        keepalive = 25
        
        try:
            with open(f"{peer_name}_private.key", "x") as f:
                f.write(private_key)
        except FileExistsError:
            # File already exists; don't overwrite DEBUG ONLY
            print(f"[!] Private key for {peer_name} already exists, not overwriting.")
            # Or log this, flash a warning, etc.

        # Append peer to config
        with open(config.WG_CONFIG_PATH, "a") as f:
            f.write(f"#{peer_name}\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {allowed_ips}\nPersistentKeepalive = {keepalive}\n")

        # Apply new config
        subprocess.run(["sudo", "wg", "addconf", config.WG_INTERFACE, config.WG_CONFIG_PATH], check=True)

        return private_key, public_key

    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise RuntimeError("Failed to execute system command.")

    except IOError as e:
        logging.error(f"I/O error: {e}")
        raise RuntimeError("Failed to write to configuration file.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError("An unexpected error occurred.")