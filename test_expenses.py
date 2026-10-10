import contextlib
import io
import os
import tempfile
import unittest

import db
import expenses


class DbTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")

    def test_to_cents(self):
        self.assertEqual(db.to_cents("12.50"), 1250)
        self.assertEqual(db.to_cents("0.1"), 10)
        self.assertEqual(db.to_cents("3"), 300)
        self.assertEqual(db.to_cents("12.345"), 1235)

    def test_bad_amounts_are_rejected(self):
        for bad in ("abc", "-5", "0", "nan", "inf", "1e999", "0.001", "99999999999999999999"):
            with self.assertRaises(ValueError):
                db.to_cents(bad)

    def test_add_and_list(self):
        db.add(self.conn, 1250, "food", "lunch", day="2026-01-02")
        self.assertEqual(db.list_all(self.conn), [(1, "2026-01-02", 1250, "food", "lunch")])

    def test_totals_biggest_first(self):
        db.add(self.conn, 500, "food")
        db.add(self.conn, 1500, "rent")
        db.add(self.conn, 700, "food")
        self.assertEqual(db.totals(self.conn), [("rent", 1500), ("food", 1200)])

    def test_remove(self):
        new_id = db.add(self.conn, 500, "food")
        self.assertTrue(db.remove(self.conn, new_id))
        self.assertFalse(db.remove(self.conn, new_id))

    def test_quotes_in_text_are_safe(self):
        db.add(self.conn, 400, "coffee", "Sam's \"best\" cafe; DROP TABLE expenses;--")
        self.assertEqual(len(db.list_all(self.conn)), 1)


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = expenses.main(list(argv))
        return code, out.getvalue()

    def test_add_then_list(self):
        with tempfile.TemporaryDirectory() as folder:
            os.environ["EXPENSES_DB"] = os.path.join(folder, "test.db")
            self.assertEqual(self.run_cli("add", "4.20", "Coffee")[1], "Added #1: 4.20 coffee\n")
            self.assertIn("4.20", self.run_cli("list")[1])

    def test_bad_amount_exits_with_error(self):
        with tempfile.TemporaryDirectory() as folder:
            os.environ["EXPENSES_DB"] = os.path.join(folder, "test.db")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    self.run_cli("add", "abc", "food")
            self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
