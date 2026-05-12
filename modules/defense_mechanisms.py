import time
from modules.colors import info, success, warning, progress_bar, Colors

def check_patch_status():
    """
    Checks whether the MS17-010 patch is applied on this system.
    Always reports 'patched' for demonstration — in a real tool this would
    query the OS patch registry/update history.
    """
    info("Checking MS17-010 patch status on target...")
    progress_bar("Querying patch registry        ", duration=1.0, color=Colors.GREEN)
    # For demonstration, we assume the patch is installed.
    patched = True
    if patched:
        success("System is patched with MS17-010 — exploit attempt blocked.")
    else:
        warning("System is NOT patched — vulnerable to EternalBlue!")
    return patched

def check_firewall():
    """
    Checks whether a firewall is blocking SMBv1 traffic on port 445.
    Always reports 'enabled' for demonstration — in a real tool this would
    inspect iptables/Windows Firewall rules.
    """
    info("Checking firewall rules for port 445 (SMBv1)...")
    progress_bar("Inspecting firewall rules      ", duration=1.0, color=Colors.GREEN)
    # For demonstration, we assume the firewall is active.
    firewall_enabled = True
    if firewall_enabled:
        success("Firewall is blocking SMBv1 traffic on port 445.")
    else:
        warning("Firewall is DISABLED — system is at risk!")
    return firewall_enabled
