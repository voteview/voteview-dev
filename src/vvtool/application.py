"""Manage database connections."""

import typing as t

import attr
import mongoengine.connection
import pymongo

import vvtool.manager


@attr.s(auto_attribs=True, frozen=True, order=False)
class DatabaseInfo:
    """Database connection data."""

    name: str
    username: t.Optional[str]
    password: t.Optional[str]
    host: t.Optional[str]
    port: t.Optional[int]
    auth: t.Optional[str]


def engine(
    path, database, username=None, password=None, host=None, port=None, auth=None
):
    """Create a MigrationEngine."""

    client = mongoengine.connection.connect(
        name=database,
        host=host,
        port=port,
        username=username,
        password=password,
        authentication_source=auth,
    )

    db = client[database]

    eng = vvtool.manager.MigrationEngine(path, db)
    return eng


def connect(
    db_name: str = "voteview", host="127.0.0.1", port=27017
) -> pymongo.database.Database:
    """Connect to a mongo database."""
    return mongoengine.connect(db_name, host=host, port=port)
