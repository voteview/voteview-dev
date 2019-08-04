"""Representations of the Voteview data."""

from __future__ import annotations

import datetime
import typing as t

import attr
import pymongo

import vvcli.exceptions
import vvcli.utils


@vvcli.utils.lock
class MemberNokkenPoole:
    """A member's Nokken-Poole score."""

    dim1: float
    dim2: float
    number_of_votes: int


@vvcli.utils.lock
class MemberNominate:
    """A member's Nominate statistics."""

    number_of_votes: int
    number_of_errors: int
    dim1: float
    dim2: float
    total_number_of_votes: int
    geo_mean_probability: float
    conditional: int
    log_likelihood: float


@vvcli.utils.lock
class Person:
    """A human person.

    A person with multiple ICPSR numbers has multiple associated `Member`s.

    """

    born: t.Optional[int]
    biography: t.Optional[str]
    id: str
    bioguide_id: t.Optional[str]
    died: t.Optional[int]
    bioname: str


@vvcli.utils.lock
class Member:
    """An ICSPR-member.

    Some persons get more than one ICPSR number and nominate score. The `Member`
    class corresponds to the ICPSR number, not a person.

    """

    person: Person
    state_abbrev: str
    nominate: MemberNominate
    icpsr: int
    last_updated: datetime.datetime
    id: str
    born: int
    died: t.Optional[int]
    district_code: int
    party_code: int
    nokken_poole: MemberNokkenPoole
    chamber: str


@vvcli.utils.lock
class RollcallNominate:
    """Nominate statistics of a rollcall."""

    conditional: int
    spread: t.List[float]
    classified: float
    log_likelihood: float
    geo_mean_probability: float
    pre: float
    mid: t.List[float]


@vvcli.utils.lock
class Rollcall:
    """A rollcall."""

    last_updated: datetime.datetime
    vote_question: str
    legis_num: str
    vote_desc: str
    nominate: RollcallNominate
    congress: int
    id: str
    date: datetime.date
    vote_type: str
    _id: str
    session: int
    rollnumber: int
    bill_number: str
    vote_result: str
    percent_support: float
    chamber: str
    clerk_rollnumber: int


def connect(db_name: str) -> pymongo.database.Database:
    """Connect to a mongo database."""
    return pymongo.MongoClient()[db_name]


# TODO Make MemberQuery etc that has all the same fields as the actual data values but all optional.
@attr.s(auto_attribs=True, cmp=False)
class DB:
    """The Voteview database object."""

    db_name: str

    @property
    def conn(self) -> pymongo.database.Database:
        """The connection object."""
        return connect(self.db_name)

    # XXX Consider using @singledispatch for ``insert()``.
    def insert_person(self, person: Person):
        self.conn.voteview_persons.insert_one(filter=vvcli.utils.asdict(person))

    def find_person(self, person: Person):
        self.conn.voteview_persons.find_one(filter=vvcli.utils.asdict(person))

    def update_person(self, filter: Person, update: Person):
        self.conn.voteview_persons.update_one(
            filter=vvcli.utils.asdict(filter), update={"$set": update}
        )

    def delete_person(self, person: Person):
        self.conn.voteview_persons.remove_one(filter=vvcli.utils.asdict(person))

    def find_member(self, member: Member) -> Member:
        return self.conn.find_one(vvcli.utils.asdict(member))

    def insert_member(self, member: Member):
        if self.find_member(member):
            raise vvcli.exceptions.DuplicateError(member)

        if not member.person or not member.person.id:
            member = attr.evolve(member, person=self.find_person(member.person).id)
        elif not member.person:
            raise vvcli.exceptions.MissingReferent("No person matching member.")

        self.conn.voteview_members.insert(vvcli.utils.asdict(member))

    def update_member(self, filter: Member, update: Member):
        self.conn.update_one(filter=filter, update=update)

    def delete_member(self, filter: Member):
        ...
