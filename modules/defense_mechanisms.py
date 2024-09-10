def check_patch_status():
    # For demonstration, we'll assume the patch is installed.
    patched = True
    
    if patched:
        print("System is patched with MS17-010, exploit attempt blocked.")
    else:
        print("System is vulnerable to EternalBlue.")

def check_firewall():
    # Assuming the firewall blocks port 445
    firewall_enabled = True
    if firewall_enabled:
        print("Firewall is blocking SMBv1 traffic on port 445.")
    else:
        print("Firewall is disabled, system is at risk.")
