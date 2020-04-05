import csv
import hashlib
from datetime import datetime

from transactionscan.models.transaction import Transaction


class BarclaysParser:
    column_mappings = {"Date": 1, "Amount": 3, "Description": 5}

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

                date = row[self.column_mappings["Date"]]
                description = row[self.column_mappings["Description"]]
                amount = row[self.column_mappings["Amount"]]


                transaction = Transaction()
                transaction.date = datetime.strptime(
                    date, "%d/%m/%Y"
                )

                # TODO: What happens if there are valid multiple transactions in a day?
                date_desc_amount = f"{date}|{description}|{amount}"
                hash = hashlib.md5(date_desc_amount.encode())
                hexdigest = hash.hexdigest()

                transaction.reference = hexdigest
                amount = amount.strip().replace(".", "")
                if amount[0] != "-":
                    transaction.income_expense = "I"
                else:
                    transaction.income_expense = "E"
                    amount = amount[1:]
                amount = int(amount)
                transaction.amount = amount
                transaction.description = description
                transactions.append(transaction)
                transaction.account = source
        return transactions
