import socket
import time
from modules.colors import info, success, warning, error, sim_tag, real_tag, progress_bar, Colors

def scan_for_smbv1(target_ip, simulated=True):
    """
    Scans for SMBv1 vulnerability on port 445.
    In simulated mode, the scan result is always 'vulnerable' for demonstration.
    In real mode, it actually probes the target IP on port 445.
    """
    info(f"Starting SMBv1 scan on {target_ip}:445 ...")
    time.sleep(0.3)

    if simulated:
        progress_bar("Sending SMB probe packets      ", duration=1.2, color=Colors.CYAN)
        progress_bar("Analysing SMB negotiation      ", duration=1.0, color=Colors.YELLOW)
        success(f"{sim_tag()} Host {target_ip} is running SMBv1 and is potentially vulnerable.")
        return True
    else:
        info(f"{real_tag()} Probing {target_ip}:445 ...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            progress_bar("Connecting to port 445         ", duration=1.0, color=Colors.RED)
            result = sock.connect_ex((target_ip, 445))
            sock.close()
            if result == 0:
                success(f"{real_tag()} Host {target_ip} has port 445 open — potentially running SMBv1.")
                return True
            else:
                warning(f"{real_tag()} Host {target_ip} does not have port 445 open — not vulnerable.")
                return False
        except socket.gaierror:
            error(f"Could not resolve host '{target_ip}'. Please check the IP address.")
            return False
        except Exception as e:
            error(f"Scan failed: {e}")
            return False
