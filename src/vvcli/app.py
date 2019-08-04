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

    dim1: float = vvcli.utils.UNSET
    dim2: float = vvcli.utils.UNSET
    number_of_votes: int = vvcli.utils.UNSET


@vvcli.utils.lock
class MemberNominate:
    """A member's Nominate statistics."""

    number_of_votes: int = vvcli.utils.UNSET
    number_of_errors: int = vvcli.utils.UNSET
    dim1: float = vvcli.utils.UNSET
    dim2: float = vvcli.utils.UNSET
    total_number_of_votes: int = vvcli.utils.UNSET
    geo_mean_probability: float = vvcli.utils.UNSET
    conditional: int = vvcli.utils.UNSET
    log_likelihood: float = vvcli.utils.UNSET


@vvcli.utils.lock
class Person:
    """A human person.

    A person with multiple ICPSR numbers has multiple associated `Member`s.

    """

    born: t.Optional[int] = vvcli.utils.UNSET
    biography: t.Optional[str] = vvcli.utils.UNSET
    id: str = vvcli.utils.UNSET
    bioguide_id: t.Optional[str] = vvcli.utils.UNSET
    died: t.Optional[int] = vvcli.utils.UNSET
    bioname: str = vvcli.utils.UNSET


@vvcli.utils.lock
class Member:
    """An ICSPR-member.

    Some persons get more than one ICPSR number and nominate score. The `Member`
    class corresponds to the ICPSR number, not a person.

    """

    person: Person = vvcli.utils.UNSET
    state_abbrev: str = vvcli.utils.UNSET
    nominate: MemberNominate = vvcli.utils.UNSET
    icpsr: int = vvcli.utils.UNSET
    last_updated: datetime.dateti = vvcli.utils.UNSETme
    id: str = vvcli.utils.UNSET
    born: int = vvcli.utils.UNSET
    died: t.Optional[int] = vvcli.utils.UNSET
    district_code: int = vvcli.utils.UNSET
    party_code: int = vvcli.utils.UNSET
    nokken_poole: MemberNokkenPoole = vvcli.utils.UNSET
    chamber: str = vvcli.utils.UNSET


@vvcli.utils.lock
class RollcallNominate:
    """Nominate statistics of a rollcall."""

    conditional: int = vvcli.utils.UNSET
    spread: t.List[float] = vvcli.utils.UNSET
    classified: float = vvcli.utils.UNSET
    log_likelihood: float = vvcli.utils.UNSET
    geo_mean_probability: float = vvcli.utils.UNSET
    pre: float = vvcli.utils.UNSET
    mid: t.List[float] = vvcli.utils.UNSET


@vvcli.utils.lock
class Rollcall:
    """A rollcall."""

    last_updated: datetime.datetime = vvcli.utils.UNSET
    vote_question: str = vvcli.utils.UNSET
    legis_num: str = vvcli.utils.UNSET
    vote_desc: str = vvcli.utils.UNSET
    nominate: RollcallNominate = vvcli.utils.UNSET
    congress: int = vvcli.utils.UNSET
    id: str = vvcli.utils.UNSET
    date: datetime.date = vvcli.utils.UNSET
    vote_type: str = vvcli.utils.UNSET
    _id: str = vvcli.utils.UNSET
    session: int = vvcli.utils.UNSET
    rollnumber: int = vvcli.utils.UNSET
    bill_number: str = vvcli.utils.UNSET
    vote_result: str = vvcli.utils.UNSET
    percent_support: float = vvcli.utils.UNSET
    chamber: str = vvcli.utils.UNSET
    clerk_rollnumber: int = vvcli.utils.UNSET


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
