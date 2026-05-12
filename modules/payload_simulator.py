import socket
import time
from modules.colors import info, success, warning, error, sim_tag, real_tag, progress_bar, Colors

def simulate_payload(target_ip, simulated=True):
    """
    Simulates the delivery of a WannaCry-style ransomware payload via port 445.
    In simulated mode, payload delivery always 'succeeds' for demonstration.
    In real mode, it attempts to send data over an actual TCP connection.
    """
    info(f"Preparing ransomware payload for delivery to {target_ip}...")
    time.sleep(0.3)

    if simulated:
        progress_bar("Injecting into process memory  ", duration=1.0, color=Colors.RED)
        progress_bar("Encrypting target filesystem   ", duration=1.4, color=Colors.RED)
        progress_bar("Dropping ransom note           ", duration=0.8, color=Colors.YELLOW)
        success(f"{sim_tag()} Payload delivered! Target files encrypted.")
        return True
    else:
        payload = b"WANNACRY_PAYLOAD_SIMULATION: Encrypt files and demand ransom."
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(3)
            progress_bar("Connecting to target           ", duration=1.0, color=Colors.RED)
            sock.connect((target_ip, 445))
            info(f"{real_tag()} Connected to {target_ip}:445")
            sock.sendall(payload)
            success(f"{real_tag()} Payload delivered to {target_ip}!")
            return True
        except ConnectionRefusedError:
            warning(f"Payload delivery failed: Connection to {target_ip}:445 refused.")
            return False
        except socket.timeout:
            warning(f"Payload delivery failed: Connection to {target_ip}:445 timed out.")
            return False
        except socket.gaierror:
            error(f"Could not resolve host '{target_ip}'. Please check the IP address.")
            return False
        except Exception as e:
            error(f"Payload delivery failed: {e}")
            return False
        finally:
            sock.close()
