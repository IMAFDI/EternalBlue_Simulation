#!/usr/bin/env python3
"""
email_finder.py — find accounts associated with an email you own.

Use this to locate stale accounts tied to an old email address so you can log
in, recover, or ask the service to delete them.

    python3 email_finder.py you@example.com
    HIBP_API_KEY=xxxx python3 email_finder.py you@example.com

What it does (all legitimate, self-service signals):
  1. Gravatar   — public profile you created; may list linked social accounts.
  2. HIBP       — data breaches containing the email (= services you signed up
                  for). Needs a free-ish API key in HIBP_API_KEY.
  3. holehe     — optional: if installed, checks ~120 sites for registration
                  via their own reset/register endpoints ('pip install holehe').
  4. Checklist  — official 'forgot password' links for Meta/Instagram/LinkedIn
                  etc. Start a reset; if the account exists the email lands in
                  the inbox you control. That's your proof and your way in.

IMPORTANT: run this only against an inbox you control. It is a tool for
cleaning up your own footprint, not for investigating other people.
"""

import argparse
import os
import re
import sys

from modules.colors import Colors, section, info, success, warning, error
from modules import email_discovery as ed

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def valid_email(value):
    if not EMAIL_RE.match(value):
        raise argparse.ArgumentTypeError(f"'{value}' does not look like an email.")
    return value.strip().lower()


def print_gravatar(res):
    section("1. Gravatar (public profile)")
    if res.get("found"):
        success(res["detail"])
        if res.get("profile_url"):
            info(f"Profile: {res['profile_url']}")
        for acct in res.get("accounts", []):
            name = acct.get("name", "link")
            url = acct.get("url", "")
            print(f"      {Colors.GREEN}→{Colors.RESET} {name}: {url}")
    else:
        info(res.get("detail", "Nothing found."))


def print_hibp(res):
    section("2. Have I Been Pwned (breach exposure)")
    if res.get("found"):
        warning(res["detail"])
        info("Each breach below is a service the email was registered on:")
        for b in res.get("breaches", []):
            line = b["name"]
            if b.get("domain"):
                line += f"  ({b['domain']})"
            if b.get("date"):
                line += f"  — {b['date']}"
            print(f"      {Colors.YELLOW}→{Colors.RESET} {line}")
    else:
        info(res.get("detail", "Nothing found."))


def print_holehe(res):
    section("3. holehe (account existence across ~120 sites)")
    if not res.get("available"):
        info(res.get("detail", "Not available."))
        return
    if res.get("sites"):
        success(res["detail"])
        for s in res["sites"]:
            print(f"      {Colors.GREEN}→{Colors.RESET} {s}")
    else:
        info(res.get("detail", "No used accounts reported."))


def print_checklist(email, items):
    section("4. Self-service checklist (do these by hand)")
    info(
        "These platforms won't confirm accounts to a script. Open each link, "
        "enter your email, and start a password reset:"
    )
    info(
        "if a reset email arrives, the account exists — and you can then log in "
        "or request deletion."
    )
    print()
    for it in items:
        print(f"  {Colors.CYAN}▸ {it['platform']}{Colors.RESET}")
        print(f"      {it['action']}")
        print(f"      {Colors.BLUE}{it['url']}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Find accounts associated with an email you own."
    )
    parser.add_argument("email", type=valid_email, help="the email address to check")
    parser.add_argument(
        "--no-network",
        action="store_true",
        help="skip online lookups; only print the manual checklist",
    )
    args = parser.parse_args()
    email = args.email

    print(f"\n  {Colors.BOLD}Email account discovery{Colors.RESET}")
    print(f"  Target inbox: {Colors.CYAN}{email}{Colors.RESET}")
    warning("Only run this against an inbox you own or control.")

    if not args.no_network:
        if ed.requests is None:
            error("The 'requests' package is missing. Run: pip install requests")
            error("Falling back to the manual checklist only.\n")
        else:
            print_gravatar(ed.check_gravatar(email))
            print_hibp(ed.check_hibp(email, os.environ.get("HIBP_API_KEY")))
            print_holehe(ed.run_holehe(email))

    print_checklist(email, ed.manual_checklist(email))

    section("Next steps")
    info("For any account you find:")
    print(f"      {Colors.WHITE}1.{Colors.RESET} Reset the password (email goes to this inbox).")
    print(f"      {Colors.WHITE}2.{Colors.RESET} Log in and either delete the account or update the email.")
    print(f"      {Colors.WHITE}3.{Colors.RESET} If you can't log in, use the service's data-deletion /")
    print(f"         privacy request form and cite this email address.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
