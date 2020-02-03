"""Command-line interface for Voteview database."""

import functools
import logging
import pathlib
import types

import click

import vvtool.application


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
    def wrapper(ctx, database, username, password, host, port, auth, path, *a, **kw):

        ctx.obj.db_info = db = vvtool.application.DatabaseInfo(
            name=database,
            username=username,
            password=password,
            host=host,
            port=port,
            auth=auth,
        )

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

    return wrapper


path_option = click.option(  # pylint: disable=invalid-name
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
@db_context
def create(ctx, name):
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
