import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080, 8443]

def scan_ports(ip, timeout=0.5):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = get_service_name(port)
                open_ports.append({"port": port, "service": service, "status": "open"})
            sock.close()
        except Exception:
            pass
    return open_ports

def get_service_name(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    return services.get(port, "Unknown")
