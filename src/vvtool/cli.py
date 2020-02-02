"""Command-line interface for Voteview database."""

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

    ctx.obj = types.SimpleNamespace()
    ctx.obj.db_info = vvtool.application.DatabaseInfo(
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

    db = ctx.obj.db_info

    path = pathlib.Path(path)
    path.mkdir(exist_ok=True, parents=True)
    import q

    q(path)

    ctx.obj.engine = vvtool.application.engine(
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

    print(ctx.obj.engine.__class__.__bases__)

    ctx.obj.engine.show_status()


@migration.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """Create a new migration.

    Specify a name for the migration.
    """
    ctx.obj.engine.create(name)


@migration.command()
@click.argument("migration_id", required=False, type=int)
@click.option("--dry-run", is_flag=True, help="Don't actually run it.")
@click.pass_context
def up(ctx, migration_id, dry_run):
    """Upgrade the database to a specified migration."""
    import q

    q(vars(ctx.obj["migrations_info"]))

    ctx.obj.engine.up(migration_id, dry_run)


@migration.command()
@click.argument("migration_id", type=int)
@click.pass_context
def down(ctx, migration_id):
    """Downgrade the database to a specified migration."""

    ctx.obj.engine.down(migration_id)
