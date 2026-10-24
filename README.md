# RPS Employee Portal

Internal staff portal for **Rock Papers Scissors** (Bengaluru): attendance, leaves, employee-to-employee tasks, payslips, ID and visiting cards, an HR desk, and a founder view with performance scorecards.

The live portal runs as a Claude artifact. This repository is the source of truth and the backup.

## What it does

| Who | What they get |
| --- | --- |
| **Employee** | Punch in and out, leave balance and requests, insurance card, tasks from colleagues (accept / decline / update / mark done), payslips, ID and visiting card. Logging out requires a work report of at least 50 words. |
| **HR desk** (people with edit access to the artifact) | Create Employee IDs (no self sign-up), edit profiles with a 6-digit code emailed to the employee, reset passwords, remove employees, run payroll, read work reports. |
| **Founder** (`RPS001`, an account with `owner: true`) | Company overview, attendance and delivery charts, department health, ranked scorecard with a per-person report, company-wide task board, plus all HR tools. |

## Files

```
index.html                 the whole portal: one self-contained page
tools/gen_demo_data.py     builds a fake team and data from 1 Aug 2026 to today, for testing
```

## How it stores data

The page uses the Claude artifact runtime (`window.claude.use(...)`):

- `db`: three collections
  - `accounts`: one document per employee (`u_<ID>`). Only people with edit access can write.
  - `hr`: payslips (`k_ems_pay_<ID>`). Only people with edit access can write.
  - `portal`: attendance, leaves and work reports (`k_ems_d_<ID>`) and tasks (`k_ems_t_<taskId>`). Any signed-in employee can write.
- `user`: decides who sees the HR desk (people with edit access).
- `mcp` → Gmail `send_message`: sends verification codes and login details from HR's Gmail.

Opened outside Claude (for example from GitHub Pages or as a local file), the page falls back to the browser's own storage. That is fine for a demo but **not** for real use: each person would only see their own browser's data.

## Demo data

```bash
FOUNDER_PASSWORD='choose-one' python3 tools/gen_demo_data.py
```

This writes one JSON file per database document into `tools/seed/` (ignored by git), plus `tools/seed_local.json` for testing the page in a browser without Claude. Every generated record carries `demo: true`; the portal's **Remove demo data** button (Employees page) deletes them all in one go. Demo employees `RPS002`–`RPS028` share a test password set in the script.

## Known limits

- Passwords are hashed in the browser and accounts are readable by anyone who can open the artifact. Keep the artifact shared only with staff.
- Closing the tab skips the logout work report; the HR reports page shows those days as "No report".
- The viewer cannot print, so cards and payslips are view-only for now.

## Roadmap: running it as our own website

To open it on any phone without a Claude account (for example `portal.rockpapersscissors.in`):

1. Host `index.html` on Vercel or GitHub Pages.
2. Replace the storage layer (`ld` / `sv` / `rm` in the script) with Supabase: Postgres tables, row-level security so only HR writes accounts and payroll, and real logins with password reset.
3. Send emails through a transactional email service instead of HR's Gmail.
