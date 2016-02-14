#!/usr/bin/env python3

import argparse
import contextlib
import errno
import fasteners
import os
from pathlib import Path
import sys

import grailfile_utils as gfutils
import utils

def cmd_init_grailfile(args):
    """Initialise the project with a new Grailfile."""
    grailfile_path = Path.cwd() / 'Grailfile'
    grailfile_path.touch(exist_ok=False)

def cmd_add_pkg(args):
    """Add a package to the manifest."""
    with gfutils.find() as grailfile:
        grailfile.add_pkg(args.pkgname)

def cmd_rm_pkg(args):
    """Remove a package from this project."""
    with gfutils.find() as grailfile:
        grailfile.rm_pkg(args.pkgname)

def main():
    parser = argparse.ArgumentParser(description='Manage packages and dependencies for Chalice programs.')
    parser.add_argument('--debug', action='store_true')

    subparsers = parser.add_subparsers(dest='subcommand', metavar='<command>')
    subparsers.required = True

    parser_init_grailfile = subparsers.add_parser('init-grailfile')
    parser_init_grailfile.set_defaults(func=cmd_init_grailfile)

    parser_add_pkg = subparsers.add_parser('add-pkg')
    parser_add_pkg.add_argument('pkgname', metavar='package-name@x.y.z')
    parser_add_pkg.set_defaults(func=cmd_add_pkg)

    parser_rm_pkg = subparsers.add_parser('rm-pkg')
    parser_rm_pkg.add_argument('pkgname', metavar='package-name')
    parser_rm_pkg.set_defaults(func=cmd_rm_pkg)

    args = parser.parse_args()
    if args.debug:
        args.func(args)
    else: 
        try:
            args.func(args)
        except utils.GrailError as exc:
            print('ERROR:', exc, file=sys.stderr)

if __name__ == '__main__':
    main()
