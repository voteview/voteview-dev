"""Command-line interface for Voteview database."""

import pathlib

import alley
import click


PACKAGE_DIR = pathlib.Path(__file__).parent

# pylint: disable=invalid-name
cli = click.Group(help="Tools for the Voteview database.")


@cli.group()
@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
    default=PACKAGE_DIR,
)
@click.option("--database", "-d", required=True, help="The database name")
@click.option("--username", "-u", help="The database user's username")
@click.option("--password", "-w", help="The database user's password")
@click.option("--host", "-h", help="The database host")
@click.option("--port", "-p", type=int, help="The database port")
@click.option("--auth", "-a", help="Authentication")
@click.pass_context
def migrate(ctx, path, database, username, password, host=None, port=None, auth=None):
    """Upgrade or downgrade the database with migrations."""
    ctx.obj = alley.MongoMigrations(
        path, database, username, password, host=host, port=port, auth=auth
    )


@migrate.command()
@click.pass_obj
def status(ctx):
    """Check the current database migration status."""
    migrations = ctx.migrations
    migrations.show_status()


@migrate.command()
@click.argument("name")
@click.pass_obj
def create(ctx, name):
    """Create a new migration.

    Specify a name for the migration.
    """
    migrations = ctx.migrations
    migrations.create(name)


@migrate.command()
@click.argument("migration_id", required=False, type=int)
@click.option("--dry-run", "fake", is_flag=True, help="Don't actually run it.")
@click.pass_obj
def up(ctx, migration_id, fake):
    """Upgrade the database to a specified migration."""
    migrations = ctx.migrations
    migrations.up(migration_id, fake)


@migrate.command()
@click.argument("migration_id", type=int)
@click.pass_obj
def down(ctx, migration_id):
    """Downgrade the database to a specified migration."""
    migrations = ctx.migrations
    migrations.down(migration_id)


if __name__ == "__main__":
    cli()
