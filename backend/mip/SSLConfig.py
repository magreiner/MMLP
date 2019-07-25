from dataclasses import dataclass


@dataclass
class SSLConfig:
    server_side: bool
    certfile: str
    keyfile: str
    ca_certs: str
