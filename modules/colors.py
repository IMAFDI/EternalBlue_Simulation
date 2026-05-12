"""
Terminal colour, formatting, and progress bar helpers.
Uses ANSI escape codes — works on Linux, macOS, and Windows 10+.
"""

import sys
import time


class Colors:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"


def banner():
    print(f"""
{Colors.RED}{Colors.BOLD}
 ███████╗████████╗███████╗██████╗ ███╗   ██╗ █████╗ ██╗      ██████╗ ██╗     ██╗   ██╗███████╗
 ██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██║     ██╔══██╗██║     ██║   ██║██╔════╝
 █████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║███████║██║     ██████╔╝██║     ██║   ██║█████╗
 ██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║     ██╔══██╗██║     ██║   ██║██╔══╝
 ███████╗   ██║   ███████╗██║  ██║██║ ╚████║██║  ██║███████╗██████╔╝███████╗╚██████╔╝███████╗
 ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
{Colors.RESET}
{Colors.YELLOW}{Colors.BOLD}              EternalBlue / MS17-010 Educational Simulation Tool{Colors.RESET}
{Colors.DIM}              For educational purposes only. Do not use on unauthorised systems.{Colors.RESET}
""")


def info(msg):
    print(f"  {Colors.CYAN}[*]{Colors.RESET} {msg}")

def success(msg):
    print(f"  {Colors.GREEN}[+]{Colors.RESET} {Colors.GREEN}{msg}{Colors.RESET}")

def warning(msg):
    print(f"  {Colors.YELLOW}[!]{Colors.RESET} {Colors.YELLOW}{msg}{Colors.RESET}")

def error(msg):
    print(f"  {Colors.RED}[-]{Colors.RESET} {Colors.RED}{msg}{Colors.RESET}")

def section(title):
    print(f"\n  {Colors.MAGENTA}{Colors.BOLD}{'─' * 50}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{Colors.BOLD}{'─' * 50}{Colors.RESET}")

def sim_tag():
    return f"{Colors.YELLOW}[SIMULATED]{Colors.RESET}"

def real_tag():
    return f"{Colors.RED}[LIVE]{Colors.RESET}"


def progress_bar(label, duration=1.5, width=35, color=Colors.CYAN):
    """
    Displays an animated progress bar in the terminal.

    Args:
        label   : Text shown to the left of the bar.
        duration: Total time in seconds the bar takes to fill.
        width   : Character width of the bar.
        color   : ANSI colour code for the filled portion.
    """
    steps = width
    delay = duration / steps
    sys.stdout.write(f"  {Colors.CYAN}[*]{Colors.RESET} {label}  [")
    sys.stdout.flush()
    for _ in range(steps):
        time.sleep(delay)
        sys.stdout.write(f"{color}█{Colors.RESET}")
        sys.stdout.flush()
    sys.stdout.write(f"] {Colors.GREEN}Done{Colors.RESET}\n")
    sys.stdout.flush()


def summary_table(results: dict, target_ip: str, mode: str):
    """
    Prints a formatted summary table of all step results.

    Args:
        results  : Dict of { step_name: (status_str, passed_bool) }
        target_ip: The IP that was targeted.
        mode     : 'Simulated' or 'Live'
    """
    col_w = 36
    val_w = 20
    divider = f"  {Colors.MAGENTA}{'═' * (col_w + val_w + 5)}{Colors.RESET}"

    print(f"\n{divider}")
    print(f"  {Colors.BOLD}{Colors.WHITE}{'SIMULATION REPORT':^{col_w + val_w + 3}}{Colors.RESET}")
    print(divider)
    print(f"  {Colors.DIM}  Target IP : {Colors.RESET}{Colors.CYAN}{target_ip}{Colors.RESET}")
    print(f"  {Colors.DIM}  Mode      : {Colors.RESET}{Colors.YELLOW if mode == 'Simulated' else Colors.RED}{mode}{Colors.RESET}")
    print(divider)
    print(f"  {Colors.BOLD}  {'Step':<{col_w}} {'Result':<{val_w}}{Colors.RESET}")
    print(f"  {Colors.MAGENTA}{'─' * (col_w + val_w + 3)}{Colors.RESET}")

    for step, (status, passed) in results.items():
        colour = Colors.GREEN if passed else Colors.RED
        icon   = "✔" if passed else "✘"
        print(f"  {Colors.WHITE}  {step:<{col_w}}{Colors.RESET} {colour}{icon}  {status}{Colors.RESET}")

    print(divider)
    all_passed = all(p for _, p in results.values())
    overall = (f"{Colors.GREEN}All steps completed successfully.{Colors.RESET}"
               if all_passed else
               f"{Colors.YELLOW}Some steps were skipped or failed — see above.{Colors.RESET}")
    print(f"  {Colors.BOLD}  Overall: {Colors.RESET}{overall}")
    print(f"{divider}\n")
