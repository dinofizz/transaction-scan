from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    func,
    extract,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from transactionscan.models.transaction import Transaction as ModelTransaction

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    amount = Column(Integer)
    account = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category")
    description = Column(String)
    income_expense = Column(String)
    reference = Column(String)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    string_matches = relationship("CategoryMatch")


class CategoryMatch(Base):
    __tablename__ = "category_match"

    id = Column(Integer, primary_key=True)
    match_string = Column(String, unique=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category")


class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)

    def get_matched_category(self, description: str):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = session.query(CategoryMatch)
        result = None
        for category_match in query.all():
            if category_match.match_string in description.lower():
                result = category_match.category.name
        session.close()
        return result

    def _get_category(self, category_name: str):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = session.query(Category).filter_by(name=category_name)
        result = None
        if query.count() > 0:
            result = query.first()
        session.close()
        return result

    def add_category_match(self, match_string: str, category_name: str):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        category_name = category_name.lower()
        match_string = match_string.lower()

        query = session.query(Category).filter_by(name=category_name)
        if query.count() <= 0:
            print(f"Error: Category {category_name} not in db.")
            session.close()
            exit(1)

        category = query.first()

        query = session.query(CategoryMatch).filter(
            CategoryMatch.match_string == match_string,
            CategoryMatch.category == category,
        )

        if query.count() == 0:
            category_match = CategoryMatch(match_string=match_string, category=category)
            session.add(category_match)
            session.commit()
        else:
            session.close()

    def add_category(self, category_name: str):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        category_name = category_name.lower()
        query = session.query(Category).filter_by(name=category_name)
        if query.count() == 0:
            category = Category(name=category_name)
            session.add(category)
        session.commit()

    def add_transaction(self, transaction: ModelTransaction):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        category = self._get_category(transaction.category)
        if category is None:
            print(f"Error: Unable to find category {transaction.category}")
            session.close()
            exit(1)
        else:
            session = session.object_session(category)
        db_transaction = Transaction()
        db_transaction.description = transaction.description
        db_transaction.amount = transaction.amount
        db_transaction.reference = transaction.reference
        db_transaction.date = transaction.date
        db_transaction.category = category
        db_transaction.income_expense = transaction.income_expense
        db_transaction.account = transaction.account
        session.add(db_transaction)
        session.commit()

    @staticmethod
    def _filter_transactions(
            session, month: int, category: Category, income_expense: str
    ):
        return (
            session.query(func.sum(Transaction.amount).label("sum"))
                .filter(
                Transaction.category == category,
                Transaction.income_expense == income_expense,
            )
                .filter(extract("month", Transaction.date) == month)
                .scalar()
        )

    def analyse_month(self, month):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        categories = session.query(Category).all()

        total_income = 0
        total_expenses = 0

        for category in categories:
            print(f"{category.name}")

            income = self._filter_transactions(session, int(month), category, "I")
            if income is None:
                income = 0

            expenses = self._filter_transactions(session, int(month), category, "E")
            if expenses is None:
                expenses = 0

            income = income // 100
            expenses = expenses // 100
            total = income - expenses

            if category.name == "transfers":
                pass
            else:
                total_expenses += expenses
                total_income += income

            print(f"\tIn: {income}\n\tOut: {expenses}\n\tTotal: {total}\n\n")

        actual_total = total_income - total_expenses
        print(
            f"\nSummary (excluding transfers):\n\nTotal in: {total_income}\n"
            f"Total out: {total_expenses}\nTotal: {actual_total}"
        )

        session.close()
