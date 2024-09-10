from modules.scanner import scan_for_smbv1
from modules.exploit_simulator import simulate_exploit
from modules.payload_simulator import simulate_payload
from modules.defense_mechanisms import check_patch_status, check_firewall

def main():
    target_ip = input("Enter target IP address: ")

    # Step 1: Scan for SMBv1 vulnerability
    scan_for_smbv1(target_ip)
    
    # Step 2: Check if system is patched
    check_patch_status()
    
    # Step 3: Check firewall status
    check_firewall()
    
    # Step 4: Simulate the exploit (if vulnerable)
    simulate_exploit(target_ip)
    
    # Step 5: Simulate payload delivery
    simulate_payload(target_ip)
    
    print("Simulation complete. Remember, this is for educational purposes only!")

if __name__ == "__main__":
    main()