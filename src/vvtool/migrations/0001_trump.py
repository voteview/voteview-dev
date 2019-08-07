import codecs
import csv
import importlib.resources
import io

import vvtool.migrations.data


DATA_FILE = "initial_trump_votes.csv"
TRUMP_ICPSR = 99912


def read_votes():
    with importlib.resources.open_text(vvtool.migrations.data, DATA_FILE) as file:
        return list(csv.DictReader(file))


def up():

    for trump_vote in read_votes():
        for rollcall in vvtool.Rollcall.objects(rollcall_id=trump_vote["VoteviewID"]):
            print(rollcall)

        new_vote = {"icpsr": TRUMP_ICPSR, "cast_code": 1}
        rollcall.update(push__votes=new_vote)
        rollcall.save()


def down():
    for trump_vote in read_votes():
        [rollcall] = vvtool.Rollcall.objects(rollcall_id=trump_vote["VoteviewID"])
        rollcall.votes.update(pull__)
