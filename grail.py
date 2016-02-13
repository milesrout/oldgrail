import argparse

def init_project(args):
    """Initialise the project with a new Grailfile."""

def add_package(args):
    """Add a package to the project."""

def rm_package(args):
    """Remove a package from this project."""

parser = argparse.ArgumentParser(description='Manage packages and dependencies for Chalice programs.')

subparsers = parser.add_subparsers(dest='subcommand')
subparsers.required = True

parser_init = subparsers.add_parser('init')
parser_init.set_defaults(func=init_project)

parser_add = subparsers.add_parser('add')
parser_add.add_argument('name', metavar='package-name@x.y.z')
parser_add.set_defaults(func=add_package)

parser_rm = subparsers.add_parser('rm')
parser_rm.add_argument('name', metavar='package-name@x.y.z')
parser_rm.set_defaults(func=rm_package)

parser.parse_args()
