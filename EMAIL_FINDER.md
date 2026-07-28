# Email Account Finder

A small tool to help you find accounts tied to **an email address you own** —
so you can log back in, recover, or ask a service to delete a stale account.

> Use it on an inbox you control. It's for cleaning up your own footprint, not
> for investigating other people. Everything it does is a legitimate,
> self-service check — no login bypassing, no scraping behind authentication.

## Install

```bash
pip install -r requirements.txt          # installs 'requests'
pip install holehe                        # optional, enables step 3
```

## Run

```bash
python3 email_finder.py you@example.com

# with breach lookup enabled:
HIBP_API_KEY=your_key python3 email_finder.py you@example.com

# offline (just the manual checklist):
python3 email_finder.py you@example.com --no-network
```

## What each step does

| Step | Source | What it tells you |
|------|--------|-------------------|
| 1 | **Gravatar** | If you ever made a Gravatar with this email, it's a *public* profile that often lists your linked Twitter/X, Instagram, LinkedIn, and websites. A strong, direct trail. |
| 2 | **Have I Been Pwned** | Which known data breaches contain the email. Every breach is a service you signed up for. Needs an API key (`HIBP_API_KEY`) from <https://haveibeenpwned.com/API/Key>. |
| 3 | **holehe** *(optional)* | The well-known open-source tool that checks ~120 sites for registration using each site's own password-reset / signup endpoint. Only runs if you install it. |
| 4 | **Self-service checklist** | Official "forgot password" links for Google, Meta/Facebook, Instagram, LinkedIn, X, Microsoft, GitHub. |

## Why "scrape the whole internet" isn't the method

Search engines deliberately don't map emails to accounts — that would be a
privacy disaster, so the data isn't indexed. The reliable signals are the ones
above: a public profile you made (Gravatar), breach records (HIBP), and each
site's own reset flow.

The big platforms (Meta, Instagram, LinkedIn) intentionally refuse to confirm
whether an account exists to an anonymous request. The correct, privacy-
respecting way to check is to **start a password reset**: if an account exists,
the reset email arrives in the inbox you control. That single fact is both your
proof the account exists *and* your way back in — which is why access to the old
mailbox (or recovering the Google account itself) is the key that unlocks the
rest.

## Once you find an account

1. Reset the password — the email lands in this inbox.
2. Log in, then delete the account or change its email away from the old one.
3. Can't log in? Use the service's **data-deletion / privacy request** form and
   cite this email address. Under GDPR/CCPA many services must action it.
