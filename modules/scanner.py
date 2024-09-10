import nmap

def scan_for_smbv1(target_ip):
    nm = nmap.PortScanner()
    # Scan for open SMB ports (Port 445)
    nm.scan(target_ip, '445')
    
    if nm[target_ip].has_tcp(445) and nm[target_ip]['tcp'][445]['state'] == 'open':
        print(f"Host {target_ip} is running SMBv1 and is potentially vulnerable.")
    else:
        print(f"Host {target_ip} is not vulnerable.")
