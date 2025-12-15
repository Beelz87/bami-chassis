import socket
from typing import List, Dict

class DNSServiceDiscovery:
    def discover(self, service_name: str) -> List[Dict]:
        try:
            ip = socket.gethostbyname(service_name)
            return [{"address": ip, "port": 80}]  # default cluster port
        except socket.gaierror:
            return []
