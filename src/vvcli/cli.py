"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mvvcli` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``vvcli.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``vvcli.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

from vvcli import app


rollcall = click.Command("rollcall")
member = click.Command("member")
vote = click.Command("vote")
person = click.Command("person")
objects = [rollcall, member, vote, person]


def group(*args, commands, **kwargs):
    return click.Group(*args, commands={c.name: c for c in commands}, **kwargs)


find = group("find", commands=objects)
update = group("update", commands=objects)
insert = group("insert", commands=objects)
delete = group("delete", commands=objects)


cli = group(commands=[find, update, insert, delete])


@cli.resultcallback()
def callback(*a, **kw):
    print(a, kw)
