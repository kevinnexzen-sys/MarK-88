import socket

def send_wol(mac: str) -> bool:
    try:
        clean = mac.replace(":", "").replace("-", "")
        if len(clean) != 12:
            return False
        data = bytes.fromhex("FF" * 6 + clean * 16)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(data, ("255.255.255.255", 9))
        s.close()
        return True
    except Exception:
        return False
