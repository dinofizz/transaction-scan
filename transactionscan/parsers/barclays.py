import csv
from datetime import datetime

from transactionscan.models.transaction import Transaction


class BarclaysParser:
    column_mappings = {"Date": 1, "Reference": 6, "Amount": 3, "Description": 5}

    def __init__(self):
        pass

    def parse(self, input_file: str, source: str):
        transactions = []
        with open(input_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            first_line = True
            for row in csv_reader:
                if first_line:
                    # In the Barclays CSV file the first row are the column names
                    first_line = False
                    continue

                # It seems that the Barclays CSV contains a last row of empty values (just commas)
                empty_row = True
                for val in row:
                    if val.strip() != "":
                        empty_row = False

                if empty_row:
                    continue

                transaction = Transaction()
                transaction.date = datetime.strptime(
                    row[self.column_mappings["Date"]], "%d/%m/%Y"
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
