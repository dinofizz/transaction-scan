import csv
from datetime import datetime

from transactionscan.models.transaction import Transaction


class MonzoParser:
    column_mappings = {"Date": 1, "Reference": 0, "Amount": 2, "Description": 8}

    def __init__(self):
        pass

    def parse(self, input_file: str, source: str):
        transactions = []
        with open(input_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            first_line = True
            for row in csv_reader:
                if first_line:
                    # In the Monzo CSV file the first row are the column names
                    first_line = False
                    continue
                transaction = Transaction()
                transaction.date = datetime.strptime(
                    row[self.column_mappings["Date"]], "%Y-%m-%dT%H:%M:%S%z"
                )
                transaction.reference = row[self.column_mappings["Reference"]]
                amount = row[self.column_mappings["Amount"]]
                amount = amount.strip().replace(".", "")
                if amount[0] != "-":
                    transaction.income_expense = "I"
                else:
                    transaction.income_expense = "E"
                    amount = amount[1:]
                amount = int(amount)
                transaction.amount = amount
                transaction.description = row[self.column_mappings["Description"]]
                transactions.append(transaction)
                transaction.account = source
        return transactions
