from datetime import datetime
import argparse


# https://stackoverflow.com/questions/25470844/specify-format-for-input-arguments-argparse-python
def valid_date(date_str):
    """
    Parses a string as a date of format YYYY-MM-DD
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_str)
        raise argparse.ArgumentTypeError(msg)


def quantify(seq, pred=None):
    "Count how many times the predicate is true in the sequence"
    return sum(map(pred, seq))
