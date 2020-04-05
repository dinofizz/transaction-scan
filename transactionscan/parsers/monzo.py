import csv
from datetime import datetime

from transactionscan.models.transaction import Transaction


class MonzoParser:
    #0             ,1   ,2   ,3   ,4   ,5    ,6       ,7     ,8       ,9           ,10            ,11             ,12     ,13     ,14         ,15
    #Transaction ID,Date,Time,Type,Name,Emoji,Category,Amount,Currency,Local amount,Local currency,Notes and #tags,Address,Receipt,Description,Category split
    column_mappings = {"Date": 1, "Name": 4, "Reference": 0, "Amount": 7, "Description": 14}

    date_format = "%d/%m/%Y"

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
                    row[self.column_mappings["Date"]], self.date_format
                )
                transaction.reference = row[self.column_mappings["Reference"]]
                amount = row[self.column_mappings["Amount"]]

                if "." in amount:
                    amount = amount.strip().replace(".", "")
                else:
                    amount = f"{amount}00"

                if amount[0] != "-":
                    transaction.income_expense = "I"
                else:
                    transaction.income_expense = "E"
                    amount = amount[1:]
                amount = int(amount)
                transaction.amount = amount
                transaction.description = f"{row[self.column_mappings['Name']]}|{row[self.column_mappings['Description']]}"
                transactions.append(transaction)
                transaction.account = source
        return transactions
