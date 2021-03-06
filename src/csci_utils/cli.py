"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcsci_utils` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``csci_utils.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``csci_utils.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from csci_utils.canvas import Canvas, comments

parser = argparse.ArgumentParser(description="Command description.")
parser.add_argument(
    "names", metavar="NAME", nargs=argparse.ZERO_OR_MORE, help="A name of something."
)


def main(args=None):
    args = parser.parse_args(args=args)
    print(args.names)

   # Canvas.assignment.submit(
   #    dict(
   #         submission_type="online_url",
   #         url="https://github.com/csci-e-29/2021sp-csci-utils-khurrumM",
   #     ),
   #     comment=dict(text_comment=comments(0)),
   # )
