#!/usr/bin/env python3
"""
================================================================================
  LAW FIRM AI PLATFORM  —  Local Practice Project
  Role you are playing: AI Systems Administrator
================================================================================

This ONE program simulates a whole law-firm AI platform on your Mac.
Each part PRETENDS to be a real Microsoft cloud tool. The comments tell you
which real cloud tool each part stands in for.

  LOCAL (this Mac)            -->   REAL CLOUD (the actual job)
  ----------------------------------------------------------------
  users.json                 -->   Microsoft Entra ID (logins)
  mfa_code check             -->   Entra ID Multi-Factor Auth (MFA)
  access.json                -->   Azure RBAC (role-based access)
  cases/ folders             -->   SharePoint / iManage (document storage)
  the access check below     -->   ETHICAL WALLS (case isolation)
  call_ai()                  -->   Claude / Microsoft Copilot (the AI brain)
  logs/audit_log.txt         -->   Azure Monitor / Entra Audit Logs
  reports/cost_report.txt    -->   Azure Cost Management
  tickets/                   -->   ServiceNow / Jira (help desk)
================================================================================
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

# Where everything lives (this folder)
HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def load_json(path):
    with open(os.path.join(HERE, path)) as f:
        return json.load(f)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ----------------------------------------------------------------------------
# PHASE 8 — AUDIT LOGGING
# LOCAL: we write a line to a text file.
# REAL CLOUD: Azure Monitor / Entra ID automatically record this.
# ----------------------------------------------------------------------------
def audit(user, action, detail):
    line = f"[{now()}] user={user} | action={action} | {detail}\n"
    with open(os.path.join(HERE, "logs", "audit_log.txt"), "a") as f:
        f.write(line)


# ----------------------------------------------------------------------------
# PHASE 7 — COST TRACKING
# LOCAL: we estimate cost and save it to a file.
# REAL CLOUD: Azure Cost Management shows this on a dashboard automatically.
# ----------------------------------------------------------------------------
def track_cost(user, case, words):
    # Pretend each AI question costs a tiny amount based on text size.
    estimated_cost = round(words * 0.00002, 5)
    line = f"[{now()}] user={user} | case={case} | est_cost_usd={estimated_cost}\n"
    with open(os.path.join(HERE, "reports", "cost_report.txt"), "a") as f:
        f.write(line)
    return estimated_cost


# ----------------------------------------------------------------------------
# PHASE 1 & 2 — LOGIN (Entra ID) + MFA + find the user's group
# ----------------------------------------------------------------------------
def login():
    users = load_json("config/users.json")["users"]
    print("\n=== STEP 1: LOGIN  (this pretends to be Microsoft Entra ID) ===")
    username = input("Who are you? (sarah / david / maria): ").strip().lower()

    user = next((u for u in users if u["username"] == username), None)
    if not user:
        print("X  No such user. (Entra ID would reject this login.)")
        audit(username, "LOGIN_FAILED", "unknown user")
        return None

    password = input("Password (hint: demo123): ").strip()
    if password != user["password"]:
        print("X  Wrong password. (Entra ID would block you.)")
        audit(username, "LOGIN_FAILED", "wrong password")
        return None

    # PHASE 1 — MFA: pretends to be the phone code Entra ID sends you.
    print(f"   (Pretend a code was texted to your phone: {user['mfa_code']})")
    code = input("Enter the 6-digit MFA code: ").strip()
    if code != user["mfa_code"]:
        print("X  Wrong MFA code. (Entra ID would block you.)")
        audit(username, "LOGIN_FAILED", "wrong MFA")
        return None

    print(f"OK  Welcome, {user['full_name']}!")
    audit(username, "LOGIN_SUCCESS", f"group={user['group']}")
    return user


# ----------------------------------------------------------------------------
# PHASE 2 & 4 — ETHICAL WALL: find which case this user may open.
# LOCAL: look up access.json.
# REAL CLOUD: Azure RBAC + SharePoint permissions decide this.
# ----------------------------------------------------------------------------
def get_allowed_case(user):
    rules = load_json("config/access.json")["access_rules"]
    return rules.get(user["group"])  # e.g. "medical"


def read_case_documents(case):
    folder = os.path.join(HERE, "cases", case)
    text = ""
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename)) as f:
            text += f.read() + "\n"
    return text


# ----------------------------------------------------------------------------
# PHASE 5 & 6 — THE AI BRAIN
# LOCAL: calls OpenAI's API (your key). If no key, runs a safe offline demo.
# REAL CLOUD: this would be Claude or Microsoft Copilot.
# ----------------------------------------------------------------------------
def call_ai(question, case_documents):
    api_key = os.environ.get("OPENAI_API_KEY")

    # If you have NOT set a key, run in free offline "demo" mode.
    if not api_key:
        return ("[OFFLINE DEMO MODE — no API key set]\n"
                "Based ONLY on this case's documents, here is a sample answer:\n"
                "The documents support the defense. (Set OPENAI_API_KEY to get a real AI answer.)")

    # Build the instruction. Notice we ONLY give the AI THIS case's documents.
    # That is the ethical wall working at the AI level too.
    prompt = (
        "You are a legal research assistant. Answer the lawyer's question using "
        "ONLY the case documents provided. Do not invent facts.\n\n"
        f"CASE DOCUMENTS:\n{case_documents}\n\n"
        f"LAWYER'S QUESTION: {question}"
    )

    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[AI error: {e}]"


# ----------------------------------------------------------------------------
# PHASE 9 — SUPPORT TICKETS
# LOCAL: save a ticket file.
# REAL CLOUD: ServiceNow / Jira.
# ----------------------------------------------------------------------------
def file_ticket(user, message):
    ticket_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    path = os.path.join(HERE, "tickets", f"ticket_{ticket_id}.txt")
    with open(path, "w") as f:
        f.write(f"Ticket from: {user}\nTime: {now()}\nProblem: {message}\n")
    audit(user, "TICKET_CREATED", f"id={ticket_id}")
    print(f"OK  Ticket created: tickets/ticket_{ticket_id}.txt (goes to the admin = YOU)")


# ----------------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("  LAW FIRM AI PLATFORM  (local practice project)")
    print("  You are the AI Systems Administrator. 3 lawyers use this safely.")
    print("=" * 70)

    user = login()
    if not user:
        print("\nLogin failed. Goodbye.")
        return

    case = get_allowed_case(user)
    print(f"\n=== STEP 2: ACCESS  (Azure RBAC + Ethical Wall) ===")
    print(f"   Your group '{user['group']}' may ONLY open the '{case}' case.")
    print(f"   You CANNOT see the other two cases. (This is the ethical wall.)")

    documents = read_case_documents(case)

    while True:
        print("\n--- What do you want to do? ---")
        print("  1) Ask the AI a question about YOUR case")
        print("  2) File a support ticket")
        print("  3) Log out")
        choice = input("Choose 1 / 2 / 3: ").strip()

        if choice == "1":
            question = input("\nYour question for the AI: ").strip()
            print("\n... asking the AI (Claude/Copilot in real life) ...")
            answer = call_ai(question, documents)
            print("\n=== AI ANSWER ===")
            print(answer)
            cost = track_cost(user["username"], case, len(answer.split()))
            audit(user["username"], "AI_QUERY", f"case={case} | est_cost=${cost}")
            print(f"\n(Logged for security. Estimated cost: ${cost})")

        elif choice == "2":
            msg = input("Describe the problem: ").strip()
            file_ticket(user["username"], msg)

        elif choice == "3":
            audit(user["username"], "LOGOUT", "user logged out")
            print("Goodbye!")
            break

        else:
            print("Please type 1, 2, or 3.")


if __name__ == "__main__":
    main()
