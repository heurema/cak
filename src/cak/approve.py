"""Operator CLI for the approval queue.

    python3 -m cak.approve --store .cak/approvals list
    python3 -m cak.approve --store .cak/approvals grant <request_id> --approver vi
    python3 -m cak.approve --store .cak/approvals deny <request_id> --approver vi
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .approvals import DEFAULT_TTL_SECONDS, ApprovalError, ApprovalStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CAK approval queue")
    parser.add_argument("--store", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="list pending approval requests")

    grant = commands.add_parser("grant", help="grant a pending request")
    grant.add_argument("request_id")
    grant.add_argument("--approver", required=True)
    grant.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS)

    deny = commands.add_parser("deny", help="deny a pending request")
    deny.add_argument("request_id")
    deny.add_argument("--approver", required=True)

    args = parser.parse_args(argv)
    store = ApprovalStore(args.store)

    try:
        if args.command == "list":
            print(json.dumps(store.list_pending(), indent=2, ensure_ascii=False))
        elif args.command == "grant":
            record = store.grant(args.request_id, approver=args.approver, ttl_seconds=args.ttl)
            print(json.dumps(record, indent=2, ensure_ascii=False))
        else:
            record = store.deny(args.request_id, approver=args.approver)
            print(json.dumps(record, indent=2, ensure_ascii=False))
    except ApprovalError as error:
        print(str(error))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
