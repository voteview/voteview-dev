"""Representations of the Voteview data."""

import datetime
import typing as t

import mongoengine
from mongoengine import fields


class MemberNokkenPoole(mongoengine.EmbeddedDocument):
    """A member's Nokken-Poole score."""

    dim1: float = fields.FloatField()
    dim2: float = fields.FloatField()
    number_of_votes: int = fields.IntField()


class MemberNominate(mongoengine.EmbeddedDocument):
    """A member's Nominate statistics."""

    number_of_votes: int = fields.IntField()
    number_of_errors: int = fields.IntField()
    dim1: float = fields.FloatField()
    dim2: float = fields.FloatField()
    total_number_of_votes: int = fields.IntField()
    geo_mean_probability: float = fields.FloatField()
    conditional: int = fields.IntField()
    log_likelihood: float = fields.IntField()


class Person(mongoengine.Document):
    """A human person.

    A Person has one Member for each Congress.
    """

    born: t.Optional[int] = fields.IntField()
    biography: t.Optional[str] = fields.StringField()
    id: str = fields.StringField()
    bioguide_id: t.Optional[str] = fields.StringField()
    died: t.Optional[int] = fields.IntField()
    bioname: str = fields.StringField()
    _id = fields.ObjectIdField()
    icpsr_list = fields.ListField(fields.IntField())
    last_updated = fields.DateTimeField()

    meta = {"collection": "voteview_persons", "strict": False}


class Member(mongoengine.Document):
    """An ICSPR-member-congress.

    Some persons get more than one ICPSR number and nominate score. The `Member`
    class corresponds to the ICPSR number and Congress, not a person.

    """

    congress: int = fields.IntField()
    person_id: str = fields.ReferenceField(Person)
    state_abbrev: str = fields.StringField()
    nominate: MemberNominate = fields.EmbeddedDocumentField(MemberNominate)
    icpsr: int = fields.IntField()
    last_updated: datetime.datetime = fields.DateTimeField()
    member_id: str = fields.StringField(db_field="id")
    district_code: int = fields.IntField()
    party_code: int = fields.IntField()
    nokken_poole: MemberNokkenPoole = fields.EmbeddedDocumentField(MemberNokkenPoole)
    chamber: str = fields.StringField()

    meta = {"collection": "voteview_members", "strict": False}


class RollcallNominate(mongoengine.EmbeddedDocument):
    """Nominate statistics of a rollcall."""

    conditional: int = fields.IntField()
    spread: t.List[float] = fields.ListField(fields.IntField())
    classified: float = fields.FloatField()
    log_likelihood: float = fields.FloatField()
    geo_mean_probability: float = fields.FloatField()
    pre: float = fields.FloatField()
    mid: t.List[float] = fields.ListField(fields.FloatField())

    meta = {"strict": False}


class Vote(mongoengine.EmbeddedDocument):
    """A single member's vote on a rollcall."""

    cast_code = fields.IntField()
    icpsr = fields.IntField()
    prob = fields.FloatField()

    meta = {"strict": False}


class Rollcall(mongoengine.Document):
    """A rollcall object."""

    bill_number = fields.StringField()
    clerk_rollnumber = fields.IntField()
    congress = fields.IntField()
    session = fields.IntField()
    vote_desc = fields.StringField()
    vote_question = fields.StringField()
    rollnumber = fields.IntField()
    rollcall_id = fields.StringField(db_field="id")
    vote_type = fields.StringField()
    nominate = fields.EmbeddedDocumentField(RollcallNominate)
    vote_result = fields.StringField()
    date = fields.DateField()
    legis_num = fields.StringField()
    percent_support = fields.FloatField()
    chamber = fields.StringField()
    last_updated = fields.DateTimeField()
    votes = fields.ListField(fields.EmbeddedDocumentField(Vote))

    meta = {"collection": "voteview_rollcalls", "strict": False}
