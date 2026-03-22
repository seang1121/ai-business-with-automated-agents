"""CLI — terminal alternative to the dashboard."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import load_config
from backend.database import init_db, get_stats, get_pending_drafts, get_draft, \
    get_all_leads, get_activity_log
from backend.approval.approval_manager import approve, reject
from backend.mode import mode_banner


def cmd_status():
    """Show agent and system status."""
    config = load_config()
    init_db()
    stats = get_stats()

    print(f"\n{'='*50}")
    print(f"  {config.business.get('name', 'AI Business')}")
    print(f"  {mode_banner(config)}")
    print(f"{'='*50}")
    print(f"\n  Pending Drafts:  {stats['pending_drafts']}")
    print(f"  New Leads:       {stats['new_leads']}")
    print(f"  Total Leads:     {stats['total_leads']}")
    print(f"  Active Jobs:     {stats['active_jobs']}")
    print(f"  Completed Jobs:  {stats['completed_jobs']}")
    print(f"  Approved Drafts: {stats['approved_drafts']}")

    print(f"\n  Agents:")
    for name in ["leads", "scheduling", "reviews", "finance", "marketing", "estimating"]:
        agent_cfg = config.agents.get(name, {})
        status = "ENABLED" if agent_cfg.get("enabled", True) else "DISABLED"
        print(f"    {name:15s} [{status}]")
    print()


def cmd_drafts():
    """List pending drafts."""
    init_db()
    drafts = get_pending_drafts()
    if not drafts:
        print("\nNo pending drafts. All clear!\n")
        return

    print(f"\nPending Drafts ({len(drafts)}):")
    print(f"{'ID':>4}  {'Agent':12s}  {'Recipient':20s}  Preview")
    print(f"{'-'*4}  {'-'*12}  {'-'*20}  {'-'*40}")
    for d in drafts:
        preview = (d['draft_text'] or '')[:50].replace('\n', ' ')
        print(f"{d['id']:>4}  {d['agent']:12s}  {d['recipient_name'] or 'N/A':20s}  {preview}...")
    print()


def cmd_approve(draft_id: int):
    """Approve a draft."""
    init_db()
    result = approve(draft_id)
    if "error" in result:
        print(f"\nError: {result['error']}\n")
    else:
        print(f"\nDraft #{draft_id} APPROVED.\n")


def cmd_reject_draft(draft_id: int):
    """Reject a draft."""
    init_db()
    result = reject(draft_id)
    if "error" in result:
        print(f"\nError: {result['error']}\n")
    else:
        print(f"\nDraft #{draft_id} REJECTED.\n")


def cmd_leads():
    """List all leads."""
    init_db()
    leads = get_all_leads()
    if not leads:
        print("\nNo leads yet.\n")
        return

    print(f"\nLeads ({len(leads)}):")
    print(f"{'ID':>4}  {'Name':20s}  {'Service':30s}  {'Status':12s}")
    print(f"{'-'*4}  {'-'*20}  {'-'*30}  {'-'*12}")
    for l in leads:
        print(f"{l['id']:>4}  {l['name']:20s}  {(l['service'] or 'N/A'):30s}  {l['status']:12s}")
    print()


def cmd_activity():
    """Show recent activity log."""
    init_db()
    logs = get_activity_log(limit=20)
    if not logs:
        print("\nNo activity yet.\n")
        return

    print(f"\nRecent Activity:")
    for entry in logs:
        print(f"  [{entry['created_at']}] {entry['agent'] or 'system'}: "
              f"{entry['action']} — {entry['details']}")
    print()


def main():
    if len(sys.argv) < 2:
        print("\nUsage: python backend/cli.py <command>")
        print("\nCommands:")
        print("  status    — Show system overview")
        print("  drafts    — List pending drafts")
        print("  approve N — Approve draft #N")
        print("  reject N  — Reject draft #N")
        print("  leads     — List all leads")
        print("  activity  — Show recent activity log")
        print("  demo      — Seed demo data + show status")
        print()
        return

    cmd = sys.argv[1].lower()

    if cmd == "status":
        cmd_status()
    elif cmd == "drafts":
        cmd_drafts()
    elif cmd == "approve" and len(sys.argv) > 2:
        cmd_approve(int(sys.argv[2]))
    elif cmd == "reject" and len(sys.argv) > 2:
        cmd_reject_draft(int(sys.argv[2]))
    elif cmd == "leads":
        cmd_leads()
    elif cmd == "activity":
        cmd_activity()
    elif cmd == "demo":
        from backend.seed_demo import seed
        seed()
        cmd_status()
    else:
        print(f"\nUnknown command: {cmd}")
        main()


if __name__ == "__main__":
    main()
