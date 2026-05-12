from modules.scanner import scan_for_smbv1
from modules.exploit_simulator import simulate_exploit
from modules.payload_simulator import simulate_payload
from modules.defense_mechanisms import check_patch_status, check_firewall
from modules.colors import banner, section, success, info, warning, Colors, summary_table

def choose_mode():
    """Prompt the user to select simulated or real (live) mode."""
    print(f"\n  {Colors.BOLD}Select run mode:{Colors.RESET}")
    print(f"  {Colors.YELLOW}  [1]{Colors.RESET} Simulated Mode  — safe demo, no real network activity")
    print(f"  {Colors.RED}  [2]{Colors.RESET} Real Mode       — live network probing (only use on systems you own)\n")
    while True:
        choice = input(f"  {Colors.CYAN}Enter choice (1 or 2): {Colors.RESET}").strip()
        if choice == "1":
            return True   # simulated
        elif choice == "2":
            print(f"\n  {Colors.RED}{Colors.BOLD}WARNING:{Colors.RESET} {Colors.RED}Only target systems you own or have explicit permission to test.{Colors.RESET}")
            confirm = input(f"  {Colors.YELLOW}Type 'yes' to confirm: {Colors.RESET}").strip().lower()
            if confirm == "yes":
                return False  # real
            else:
                warning("Confirmation not given. Defaulting to Simulated Mode.")
                return True
        else:
            warning("Invalid choice. Please enter 1 or 2.")

def main():
    banner()

    # Mode selection
    simulated = choose_mode()
    mode_str   = "Simulated" if simulated else "Live"
    mode_label = (f"{Colors.YELLOW}SIMULATED{Colors.RESET}" if simulated
                  else f"{Colors.RED}LIVE{Colors.RESET}")
    print(f"\n  Mode: {mode_label}\n")

    # Target IP
    target_ip = input(f"  {Colors.CYAN}Enter target IP address: {Colors.RESET}").strip()

    # Results dict: { step_name: (status_string, passed_bool) }
    results = {}

    # Step 1: Scan for SMBv1 vulnerability
    section("Step 1 — SMBv1 Vulnerability Scan")
    vulnerable = scan_for_smbv1(target_ip, simulated=simulated)
    results["SMBv1 Vulnerability Scan"] = (
        "Vulnerable (port 445 open)" if vulnerable else "Not vulnerable",
        vulnerable
    )

    # Step 2: Check patch status
    section("Step 2 — Patch Status Check (MS17-010)")
    patched = check_patch_status()
    results["MS17-010 Patch Status"] = (
        "Patched — exploit blocked" if patched else "UNPATCHED — at risk!",
        patched
    )

    # Step 3: Check firewall status
    section("Step 3 — Firewall Status Check")
    fw_enabled = check_firewall()
    results["Firewall (port 445)"] = (
        "Enabled — traffic blocked" if fw_enabled else "DISABLED — at risk!",
        fw_enabled
    )

    # Step 4: Simulate the exploit
    section("Step 4 — EternalBlue Exploit")
    if vulnerable or simulated:
        exploit_ok = simulate_exploit(target_ip, simulated=simulated)
        results["EternalBlue Exploit"] = (
            "Exploit sent successfully" if exploit_ok else "Exploit failed / blocked",
            exploit_ok
        )
    else:
        warning("Target not vulnerable — skipping exploit step.")
        results["EternalBlue Exploit"] = ("Skipped (not vulnerable)", False)

    # Step 5: Simulate payload delivery
    section("Step 5 — Payload Delivery")
    if vulnerable or simulated:
        payload_ok = simulate_payload(target_ip, simulated=simulated)
        results["Payload Delivery"] = (
            "Payload delivered" if payload_ok else "Delivery failed / blocked",
            payload_ok
        )
    else:
        warning("Target not vulnerable — skipping payload step.")
        results["Payload Delivery"] = ("Skipped (not vulnerable)", False)

    # Summary table
    section("Simulation Report")
    summary_table(results, target_ip=target_ip, mode=mode_str)

    success("Remember: this tool is for educational purposes only!")
    print(f"  {Colors.DIM}Never use this knowledge for unauthorised access to systems.{Colors.RESET}\n")

if __name__ == "__main__":
    main()
