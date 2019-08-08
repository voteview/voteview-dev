"""Add initial Trump votes from Congressional Quarterly file."""


import csv
import typing as t

import importlib_resources

import vvtool.migrations.data


DATA_FILE = "initial_trump_votes.csv"
TRUMP_ICPSR = 99912


def read_votes() -> t.List[t.Dict[str, str]]:
    """Read Trump vote records from the data file."""
    with importlib_resources.open_text(vvtool.migrations.data, DATA_FILE) as file:
        return list(csv.DictReader(file))


def up(db=None):  # pylint: disable=unused-argument
    """Add initial Trump votes from Congressional Quarterly file."""
    for record in read_votes():
        rollcall = vvtool.Rollcall.objects(rollcall_id=record["VoteviewID"])
        new_vote = {"icpsr": TRUMP_ICPSR, "cast_code": 1}
        rollcall.update_one(push__votes=new_vote)


def down(db=None):  # pylint: disable=unused-argument
    """Remove initial Trump votes from Congressional Quarterly file."""
    for trump_vote in read_votes():
        rollcall = vvtool.Rollcall.objects(rollcall_id=trump_vote["VoteviewID"])
        new_vote = {"icpsr": TRUMP_ICPSR, "cast_code": 1}
        rollcall.update_one(pull__votes=new_vote)
