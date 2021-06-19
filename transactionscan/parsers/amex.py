import csv
from datetime import datetime

from transactionscan.models.transaction import Transaction


class AmexParser:
    column_mappings = {"Date": 0, "Reference": 11, "Amount": 4, "Description": 1}

    def __init__(self):
        pass

    def parse(self, input_file: str, source: str):
        transactions = []
        with open(input_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            first_line = True
            for row in csv_reader:
                if first_line:
                    # In the Amex CSV file the first row are the column names
                    first_line = False
                    continue

                transaction = Transaction()
                transaction.date = datetime.strptime(
                    row[self.column_mappings["Date"]], "%d/%m/%Y"
                )
                transaction.reference = row[self.column_mappings["Reference"]]
                amount = row[self.column_mappings["Amount"]]
                amount = amount.strip().replace(".", "")
                if amount[0] == "-":
                    transaction.income_expense = "I"
                    amount = amount[1:]
                amount = int(amount)
                transaction.amount = amount
                transaction.description = row[self.column_mappings["Description"]]
                transactions.append(transaction)
                transaction.account = source
        return transactions
