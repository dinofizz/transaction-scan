import argparse
import os

from transactionscan.db.db import Database
from transactionscan.parsers.amex import AmexParser
from transactionscan.parsers.barclays import BarclaysParser
from transactionscan.parsers.monzo import MonzoParser

parser_dict = {"amex": AmexParser, "monzo": MonzoParser, "barclays": BarclaysParser}
source_list = ["monzo-dino", "monzo-lau", "monzo-joint", "amex", "barclays-dino"]


def parse_input(db: Database, input_file: str, format: str, source: str):
    ParserClass = parser_dict.get(format)
    if ParserClass is None:
        print(f"Unable to find parser for {format}.")
        exit(1)
    parser = ParserClass()
    transactions = parser.parse(input_file, source)
    for transaction in transactions:
        matched_category = db.get_matched_category(transaction.description)
        if matched_category is None:
            print(
                f"Please enter a tag and category for description {transaction.description} : {transaction.amount}"
            )
            tag = input("Tag: ").lower().strip()
            if tag.strip() != "":
                category = input("Category: ").lower().strip()
                db.add_category(category)
                db.add_category_match(tag, category)
                transaction.category = category
        else:
            transaction.category = matched_category
        db.add_transaction(transaction)


def add_category(db, add_category):
    db.add_category(add_category)


def add_category_tag(db, match_string, add_category):
    db.add_category_match(match_string, add_category)


def analyse_month(db, month):
    db.analyse_month(month)


def main():
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers(help="commands")

    import_parser = subparsers.add_parser("import", help="Import transactions")
    import_parser.add_argument(
        "input-file",
        metavar="FILE",
        nargs=1,
        action="store",
        help="Original csv file containing transactions",
    )
    import_parser.add_argument(
        "format",
        metavar="FORMAT",
        nargs=1,
        action="store",
        help="Input file format",
        choices=list(parser_dict.keys()),
    )
    import_parser.add_argument(
        "source",
        metavar="SOURCE",
        nargs=1,
        action="store",
        help="Source account",
        choices=source_list,
    )

    category_parser = subparsers.add_parser("category", help="Add category")
    category_parser.add_argument(
        "category", metavar="CATEGORY", nargs=1, action="store", help="Category to add"
    )

    tag_parser = subparsers.add_parser("tag", help="Add tag")
    tag_parser.add_argument(
        "tag", metavar="TAG", nargs=1, action="store", help="Tag to add"
    )
    tag_parser.add_argument(
        "category",
        metavar="CATEGORY",
        nargs=1,
        action="store",
        help="Category to associate with tag",
    )

    analyse = subparsers.add_parser("analyse", help="Analyse month")
    analyse.add_argument(
        "month", metavar="MONTH", nargs=1, action="store", help="Month to analyse"
    )

    args = vars(arg_parser.parse_args())

    db = Database("sqlite:///db.sqlite")

    if "input-file" in args:
        parse_input(db, args["input-file"][0], args["format"][0], args["source"][0])
    elif "category" in args and "tag" not in args:
        add_category(db, args["category"][0])
    elif "tag" in args and "category" in args:
        add_category_tag(db, args["tag"][0], args["category"][0])
    elif "month" in args:
        analyse_month(db, args["month"][0])
    else:
        arg_parser.print_help()


if __name__ == "__main__":
    main()