"""Command-line interface for Voteview database."""

import functools
import logging
import pathlib
import sys
import types
import typing as t

import attr
import click
import q

import vvtool.application


q(sys.argv)


PACKAGE_DIR = pathlib.Path(__file__).parent


@click.group()
@click.pass_context
def cli(ctx):
    """Tools for the Voteview database."""

    logging.basicConfig(level=logging.DEBUG)

    ctx.obj = types.SimpleNamespace()


def db_context(func):
    """Add the database connection options."""

    @functools.wraps(func)
    @click.option("--database", "-d", help="The database name")
    @click.option("--username", "-u", help="The database user's username")
    @click.option("--password", "-w", help="The database user's password")
    @click.option("--host", "-h", help="The database host")
    @click.option("--port", "-p", type=int, help="The database port")
    @click.option("--auth", "-a", help="Authentication")
    @path_option
    @click.pass_context
    def f(ctx, database, username, password, host, port, auth, path, *a, **kw):

        ctx.obj.db_info = db = vvtool.application.DatabaseInfo(
            name=database,
            username=username,
            password=password,
            host=host,
            port=port,
            auth=auth,
        )
        print(vvtool.application.engine)
        ctx.obj.engine = vvtool.application.engine(
            path=path,
            database=db.name,
            username=db.username,
            password=db.password,
            host=db.host,
            port=db.port,
            auth=db.auth,
        )

        return func(ctx, *a, **kw)

    return f


path_option = click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
    default=PACKAGE_DIR.joinpath("migrations/"),
)


@cli.group()
def migration():
    """Upgrade or downgrade the database with migrations."""


@migration.command()
@db_context
def status(ctx):
    """Check the current database migration status."""

    print(ctx.obj.engine)
    ctx.obj.engine.show_status()


@migration.command()
@click.argument("name")
@path_option
def create(name):
    """Create a new migration.

    Specify a name for the migration.
    """
    ctx.obj.engine.create(name)


@migration.command()
@click.argument("migration_id", required=False, type=int)
@click.option("--dry-run", is_flag=True, help="Don't actually run it.")
@db_context
def up(ctx, migration_id, dry_run):
    """Upgrade the database to a specified migration."""

    ctx.obj.engine.up(migration_id, dry_run)


@migration.command()
@click.argument("migration_id", type=int)
@db_context
def down(ctx, migration_id):
    """Downgrade the database to a specified migration."""

    ctx.obj.engine.down(migration_id)
