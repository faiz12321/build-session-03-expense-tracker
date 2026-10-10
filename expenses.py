import argparse
import os
import sys

import db


def main(argv=None):
    parser = argparse.ArgumentParser(description="A tiny expense tracker.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add an expense")
    add.add_argument("amount", help="for example 12.50")
    add.add_argument("category", help="for example food")
    add.add_argument("note", nargs="?", default="", help="optional note")

    sub.add_parser("list", help="show all expenses")
    sub.add_parser("summary", help="totals per category")

    delete = sub.add_parser("delete", help="delete an expense by id")
    delete.add_argument("id", type=int)

    args = parser.parse_args(argv)
    conn = db.connect(os.environ.get("EXPENSES_DB", "expenses.db"))

    if args.command == "add":
        try:
            cents = db.to_cents(args.amount)
        except ValueError as err:
            parser.error(str(err))
        category = args.category.strip().lower()
        if not category:
            parser.error("category cannot be empty")
        new_id = db.add(conn, cents, category, args.note)
        print(f"Added #{new_id}: {db.money(cents)} {category}")
    elif args.command == "list":
        rows = db.list_all(conn)
        if not rows:
            print("No expenses yet.")
        for row_id, day, cents, category, note in rows:
            print(f"{row_id:>3}  {day}  {db.money(cents):>8}  {category:<10} {note}")
    elif args.command == "summary":
        rows = db.totals(conn)
        for category, cents in rows:
            print(f"{category:<12} {db.money(cents):>8}")
        print(f"{'total':<12} {db.money(sum(c for _, c in rows)):>8}")
    elif args.command == "delete":
        if db.remove(conn, args.id):
            print(f"Deleted #{args.id}")
        else:
            print(f"No expense #{args.id}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
