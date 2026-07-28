"""
Email account-discovery helpers.

Purpose: help a person find where *their own* email address is registered so
they can log in, recover, or request deletion of stale accounts.

Design principles
-----------------
* Only uses legitimate, self-service signals:
    - Gravatar  : a PUBLIC profile the email owner created; often lists their
                  linked social accounts.
    - HIBP      : Have I Been Pwned — which known data breaches contain the
                  email. A breach = the email was registered on that service.
    - holehe    : optional wrapper around the well-known open-source tool that
                  checks account existence via each site's own reset/register
                  endpoint. Only runs if you install it yourself.
* For the big platforms (Meta/Facebook, Instagram, LinkedIn) that deliberately
  block automated enumeration, we DON'T probe them. Instead we hand you the
  official "forgot password" links. If an account exists, the reset email lands
  in the inbox you control — that is both the proof and the recovery path.

Nothing here bypasses authentication, scrapes behind a login, or enumerates
strangers' accounts. Use it on an inbox you control.
"""

import hashlib
import json
import shutil
import subprocess
from urllib.parse import quote

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

USER_AGENT = "email-discovery-selfcheck/1.0 (personal account cleanup)"
TIMEOUT = 15


def _md5(text):
    return hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()


def _sha256(text):
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Gravatar
# --------------------------------------------------------------------------- #
def check_gravatar(email):
    """
    Look up a public Gravatar profile for the email.

    Gravatar profiles are created by the email owner and are intentionally
    public. Many list linked accounts (Twitter/X, Instagram, LinkedIn, personal
    sites), which is exactly the kind of trail you're looking for.

    Returns a dict describing what was found (or that nothing was).
    """
    result = {"service": "Gravatar", "found": False, "detail": "", "accounts": []}
    if requests is None:
        result["detail"] = "The 'requests' package is not installed."
        return result

    h = _md5(email)
    profile_url = f"https://en.gravatar.com/{h}.json"
    try:
        resp = requests.get(
            profile_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        )
    except Exception as exc:  # noqa: BLE001
        result["detail"] = f"Request failed: {exc}"
        return result

    if resp.status_code == 404:
        result["detail"] = "No public Gravatar profile."
        return result
    if resp.status_code != 200:
        result["detail"] = f"Unexpected HTTP {resp.status_code}."
        return result

    try:
        data = resp.json()
        entry = data.get("entry", [{}])[0]
    except (json.JSONDecodeError, ValueError, IndexError):
        result["detail"] = "Profile exists but could not be parsed."
        result["found"] = True
        return result

    result["found"] = True
    result["profile_url"] = entry.get("profileUrl", f"https://gravatar.com/{h}")
    result["display_name"] = entry.get("displayName", "")

    # Linked social accounts declared on the public profile.
    for acct in entry.get("accounts", []):
        result["accounts"].append(
            {
                "name": acct.get("name") or acct.get("shortname", ""),
                "url": acct.get("url", ""),
            }
        )
    # Verified/URL entries the owner added.
    for url in entry.get("urls", []):
        result["accounts"].append({"name": "website", "url": url.get("value", "")})

    n = len(result["accounts"])
    result["detail"] = (
        f"Public profile found with {n} linked account(s)/link(s)."
        if n
        else "Public profile found (no linked accounts listed)."
    )
    return result


# --------------------------------------------------------------------------- #
# Have I Been Pwned
# --------------------------------------------------------------------------- #
def check_hibp(email, api_key=None):
    """
    Query Have I Been Pwned for breaches containing the email.

    Each breach names a service the email was registered with — a direct map of
    'where did I have an account'. The breaches endpoint requires an API key
    (https://haveibeenpwned.com/API/Key). Without one, we skip gracefully.
    """
    result = {"service": "HaveIBeenPwned", "found": False, "detail": "", "breaches": []}
    if requests is None:
        result["detail"] = "The 'requests' package is not installed."
        return result
    if not api_key:
        result["detail"] = (
            "Skipped — set HIBP_API_KEY to enable. Get one at "
            "https://haveibeenpwned.com/API/Key"
        )
        return result

    url = (
        "https://haveibeenpwned.com/api/v3/breachedaccount/"
        f"{quote(email)}?truncateResponse=false"
    )
    headers = {"hibp-api-key": api_key, "User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except Exception as exc:  # noqa: BLE001
        result["detail"] = f"Request failed: {exc}"
        return result

    if resp.status_code == 404:
        result["detail"] = "Good news: no breaches on record for this email."
        return result
    if resp.status_code == 401:
        result["detail"] = "Invalid or missing HIBP API key."
        return result
    if resp.status_code == 429:
        result["detail"] = "Rate limited by HIBP — wait and retry."
        return result
    if resp.status_code != 200:
        result["detail"] = f"Unexpected HTTP {resp.status_code}."
        return result

    try:
        breaches = resp.json()
    except (json.JSONDecodeError, ValueError):
        result["detail"] = "Could not parse HIBP response."
        return result

    result["found"] = bool(breaches)
    for b in breaches:
        result["breaches"].append(
            {
                "name": b.get("Title") or b.get("Name", ""),
                "domain": b.get("Domain", ""),
                "date": b.get("BreachDate", ""),
            }
        )
    result["detail"] = f"Email appears in {len(result['breaches'])} known breach(es)."
    return result


# --------------------------------------------------------------------------- #
# holehe (optional external tool)
# --------------------------------------------------------------------------- #
def run_holehe(email):
    """
    Run 'holehe' if it is installed, returning sites where the email is
    registered. holehe is the established open-source tool for this exact task;
    we don't reimplement its ~120 site checks. Install it yourself with:
        pip install holehe
    """
    result = {"service": "holehe", "available": False, "detail": "", "sites": []}
    if shutil.which("holehe") is None:
        result["detail"] = "holehe not installed. Optional: 'pip install holehe'."
        return result

    result["available"] = True
    try:
        proc = subprocess.run(
            ["holehe", "--only-used", email],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        result["detail"] = "holehe timed out."
        return result
    except Exception as exc:  # noqa: BLE001
        result["detail"] = f"holehe failed to run: {exc}"
        return result

    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("[+]"):
            result["sites"].append(line[3:].strip())
    result["detail"] = f"holehe reports {len(result['sites'])} used account(s)."
    return result


# --------------------------------------------------------------------------- #
# Manual self-service checklist for platforms that block enumeration
# --------------------------------------------------------------------------- #
def manual_checklist(email):
    """
    Return the official self-service links for the platforms people most often
    ask about. These deliberately don't confirm account existence to strangers,
    so the correct (and privacy-respecting) way to check is to start a password
    reset: if an account exists, the email arrives in the inbox you control.
    """
    e = quote(email)
    return [
        {
            "platform": "Google account (the email itself)",
            "action": "Recover / find the account",
            "url": "https://accounts.google.com/signin/recovery",
        },
        {
            "platform": "Facebook / Meta",
            "action": "Find & reset via 'Forgot password'",
            "url": "https://www.facebook.com/login/identify",
        },
        {
            "platform": "Instagram (Meta)",
            "action": "Reset link sent to email if account exists",
            "url": "https://www.instagram.com/accounts/password/reset/",
        },
        {
            "platform": "LinkedIn",
            "action": "Forgot password → enter this email",
            "url": "https://www.linkedin.com/uas/request-password-reset",
        },
        {
            "platform": "X / Twitter",
            "action": "Password reset by email",
            "url": "https://x.com/account/begin_password_reset",
        },
        {
            "platform": "Microsoft",
            "action": "Account recovery",
            "url": "https://account.live.com/password/reset",
        },
        {
            "platform": "GitHub (if a dev account)",
            "action": f"Search commits by author-email, then reset",
            "url": "https://github.com/password_reset",
        },
    ]
