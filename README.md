# Build Session 03: an expense tracker

A small command-line expense tracker built step by step with real commands. Python and SQLite only. No packages to install.

    python3 expenses.py add 12.50 food "team lunch"
    python3 expenses.py list
    python3 expenses.py summary
    python3 expenses.py delete 1

- Data is saved in `expenses.db` in the folder you run it from (set `EXPENSES_DB` to use another file).
- Money is stored as whole cents. Text is saved safely with SQL placeholders, so quotes cannot break it.
- Bad input is refused with a clear message and a non-zero exit code.

## Run the tests

Needs Python 3 (built and tested on Python 3.10.12, SQLite 3.37.2).

    python3 -m unittest -v

8 tests. They use temporary databases, so your own data is never touched.

## Notes

- Educational example, no warranty. Use at your own risk.
- Sample expenses in the walkthrough are made-up entries.
- Code is MIT licensed (see LICENSE). Python and SQLite are separate projects with their own licenses; this repository does not include them.
