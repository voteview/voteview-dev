"""Command-line interface for Voteview database."""

import logging
import pathlib
import typing as t

import attr
import click

import vvtool.app


PACKAGE_DIR = pathlib.Path(__file__).parent


@attr.s(auto_attribs=True, frozen=True, cmp=False)
class DatabaseInfo:
    """Database connection data."""

    name: str
    username: t.Optional[str]
    password: t.Optional[str]
    host: t.Optional[str]
    port: t.Optional[int]
    auth: t.Optional[str]


@click.group()
@click.option("--database", "-d", help="The database name")
@click.option("--username", "-u", help="The database user's username")
@click.option("--password", "-w", help="The database user's password")
@click.option("--host", "-h", help="The database host")
@click.option("--port", "-p", type=int, help="The database port")
@click.option("--auth", "-a", help="Authentication")
@click.pass_context
def cli(ctx, database, username, password, host, port, auth):
    """Tools for the Voteview database."""

    logging.basicConfig(level=logging.DEBUG)

    ctx.obj = {}
    ctx.obj["db_info"] = DatabaseInfo(
        name=database,
        username=username,
        password=password,
        host=host,
        port=port,
        auth=auth,
    )


@cli.group()
@click.pass_context
@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
    default=PACKAGE_DIR.joinpath("migrations/"),
)
def migration(ctx, path):
    """Upgrade or downgrade the database with migrations."""

    db = ctx.obj["db_info"]

    path.mkdir(exist_ok=True, parent=True)

    ctx.obj["migrations_info"] = vvtool.app.MongoMigrations(
        path=path,
        database=db.name,
        username=db.username,
        password=db.password,
        host=db.host,
        port=db.port,
        auth=db.auth,
    )


@migration.command()
@click.pass_context
def status(ctx):
    """Check the current database migration status."""

    ctx.obj["migrations_info"].migrations.show_status()


@migration.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """Create a new migration.

    Specify a name for the migration.
    """
    ctx.obj["migrations_info"].migrations.create(name)


@migration.command()
@click.argument("migration_id", required=False, type=int)
@click.option("--dry-run", "fake", is_flag=True, help="Don't actually run it.")
@click.pass_context
def up(ctx, migration_id, fake):
    """Upgrade the database to a specified migration."""

    ctx.obj["migrations_info"].migrations.up(migration_id, fake)


@migration.command()
@click.argument("migration_id", type=int)
@click.pass_context
def down(ctx, migration_id):
    """Downgrade the database to a specified migration."""

    ctx.obj["migrations_info"].migrations.down(migration_id)
