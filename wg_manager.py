import subprocess 

class WgManager: 
    def __init__(self, network: str, gateway: str, listen_port: int): 
        # TODO: Parse with ipaddress module for collisions and overlaps 
        self.network = network 
        self.gateway = gateway 
        self.listen_port = listen_port 
        self.name = "wg0" 
        # TODO: custom names 
        self.peers = [] 
        # Generate wg-server interface keys 
        self.private_key, self.public_key = self.generate_keypairs() 
        print(self.private_key + "\n" + self.public_key) 

    def make_cfgfile(self): 
    # TODO: different names for different servers (multiple instances) 
        cfg = f"""[Interface] Address = {self.gateway}
ListenPort = {self.listen_port}
PrivateKey = {self.private_key}
""" 
        for peer in self.peers: 
            cfg += f"""
[Peer] # {peer["name"]}
PublicKey = {peer["public_key"]}
AllowedIPs = {peer["ip"]} """
        return cfg
    
    def add_peer(self, name: str, endpoint_ip: str):
        private_key, public_key = self.generate_keypairs()
        peer = { 
            "name": name, 
            "ip": endpoint_ip, 
            "public_key": public_key, 
            "private_key": private_key
        } 
        self.peers.append(peer)

    def build_interface(self): 
        pass 

    def get_status(self): 
        result = subprocess.run(["wg", "show"], capture_output=True, text=True)
        print(result.stdout)

    def generate_keypairs(self): 
        private_key = subprocess.run( ["wg", "genkey"],capture_output=True, text=True, check=True).stdout.strip()
        public_key = subprocess.run( ["wg", "pubkey"], input=private_key, capture_output=True, text=True, check=True).stdout.strip()
        return private_key, public_key