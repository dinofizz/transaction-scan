# transaction-scan

`transaction-scan` is a personal project to scan exports of transactions from Amex, Monzo and Barclays. Transactions are categorised and stored to a SQLite database.

## Installation

It is recommended to use a virtual environment.

First you will need to build the project:

```shell script
$ python setup.py build
```

And then you can install it:

```shell script
$ python setup.py install
```

This will download the required SQLAlchemy dependency and install a `transaction-scan` binary to your virtual environment `bin` folder.

## Usage

### Adding a category

```shell script
$ transaction-scan category                                                                                                                                                               *[master] 
usage: transaction-scan category [-h] CATEGORY
transaction-scan category: error: the following arguments are required: CATEGORY

$ transaction-scan category entertainment
```

### Adding a tag for a category

```shell script
$ transaction-scan tag                                                                                                                                                                    *[master] 
usage: transaction-scan tag [-h] TAG CATEGORY
transaction-scan tag: error: the following arguments are required: TAG, CATEGORY

$ transaction-scan tag netflix entertainment
```

### Importing a Monzo transaction export

```shell script
$ transaction-scan import                                                                                                                                                                 *[master] 
usage: transaction-scan import [-h] FILE FORMAT SOURCE
transaction-scan import: error: the following arguments are required: FILE, FORMAT, SOURCE

$ transaction-scan import exported_data.csv monzo monozo-dino
```

* FORMAT can be wither "monzo", "amex" or "barclays".
* SOURCE is an identifier for the source account.


