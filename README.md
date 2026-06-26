# 🏛️ Law Firm AI Platform — Local Practice Project

**Your role:** AI Systems Administrator
**What it does:** Lets 3 lawyers safely use AI on 3 separate secret cases — and stops anyone from seeing another case's files (ethical walls).

| Lawyer | Login | Case | Defends |
|--------|-------|------|---------|
| 👩 Sarah | `sarah` | 💊 Medical | Drug company |
| 👨 David | `david` | 🏭 Manufacturing | Machine maker |
| 👩 Maria | `maria` | 🚬 Tobacco | Cigarette company |

Password for all: `demo123` · MFA codes: Sarah `111111`, David `222222`, Maria `333333`

---

## ▶️ How to run it

```bash
cd law-firm-ai-project
python3 app.py
```

It works **with no signup** (offline demo mode).
To get **real AI answers** with your OpenAI key, run this first (paste YOUR key):

```bash
export OPENAI_API_KEY="sk-your-key-here"
python3 app.py
```

⚠️ Your key stays on your Mac. Never put it in any file you share.

---

## 🔑 THE BIG COMPARISON — Local (this Mac) vs. Real Cloud (the job)

This is the most important part. Each piece of this project **pretends** to be a real
Microsoft cloud tool. Here is exactly what each one maps to:

| # | What you do here (LOCAL 💻) | In the file/code | What it would REALLY be (CLOUD ☁️) |
|---|------------------------------|------------------|-------------------------------------|
| 1 | Log in with username | `users.json` | **Microsoft Entra ID** (identity system) |
| 2 | Enter the 6-digit code | `mfa_code` check | **Entra ID MFA** (real phone code) |
| 3 | Group decides your access | `access.json` | **Azure RBAC** (role assignments) |
| 4 | You can only open your case | the access check | **Ethical walls** (SharePoint permissions) |
| 5 | Secret case files in folders | `cases/` | **SharePoint / iManage** (document system) |
| 6 | The AI answers questions | `call_ai()` (OpenAI) | **Claude / Microsoft Copilot** |
| 7 | Connect AI to documents | code passes docs in | **APIs + Power Automate connectors** |
| 8 | Cost saved to a file | `cost_report.txt` | **Azure Cost Management** (dashboard) |
| 9 | Who-did-what saved to a file | `audit_log.txt` | **Azure Monitor / Entra Audit Logs** |
| 10 | Problems saved as tickets | `tickets/` | **ServiceNow / Jira** (help desk) |
| 11 | Admin resolves a ticket | `resolve_ticket()` | **ServiceNow / Jira** "Resolve" button |

> **The IDEA is identical. Only the SIZE and the REAL TOOLS differ.**
> Local = a free practice "dollhouse." Cloud = the giant live version a company pays for.

---

## 🧱 Want to SEE the ethical wall work?

Run `python3 prove_wall.py` — it tries to let Sarah peek at the Tobacco case and
shows that the system **blocks** her. That's the wall doing its job.

---

## 🎫 Filing and resolving support tickets

The menu (after you log in) has two ticket actions:

* **`2) File a support ticket`** — a lawyer reports a problem. It's saved as
  `tickets/ticket_<timestamp>.txt`. → *like opening a ticket in ServiceNow / Jira.*
* **`3) Resolve a support ticket (admin)`** — you, the admin, pick an open ticket
  from the list, type how you fixed it, and the app:
  1. adds a **resolution note** (status, who, when, fix) to the ticket,
  2. renames it to `RESOLVED_ticket_<timestamp>.txt` so it's clearly closed, and
  3. records a `TICKET_RESOLVED` line in `logs/audit_log.txt`.

  → *like clicking "Resolve" in ServiceNow / Jira.*

> Note: in this demo any logged-in user can resolve tickets (there's no separate
> admin login). In a real system, RBAC would restrict this to admins only.

---

## 🗂️ What's in this folder

```
law-firm-ai-project/
├── app.py              # the main program (all 10 phases)
├── prove_wall.py       # proves the ethical wall blocks cross-case access
├── config/
│   ├── users.json      # the 3 lawyers   (pretends to be Entra ID)
│   └── access.json     # who sees what   (pretends to be Azure RBAC)
├── cases/              # secret case files (pretends to be SharePoint)
│   ├── medical/
│   ├── manufacturing/
│   └── tobacco/
├── logs/               # audit_log.txt   (pretends to be Azure Monitor)
├── reports/            # cost_report.txt (pretends to be Azure Cost Mgmt)
└── tickets/            # support tickets  (pretends to be ServiceNow)
```
