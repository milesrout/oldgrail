import contextlib
import errno
import fasteners
import os
from pathlib import Path
import sys

import utils

@contextlib.contextmanager
def _open_grailfile(path):
    """Lock and open the Grailfile at the given path."""
    # if the Grailfile is foobar/Grailfile, store a lock at foobar/.grail/LOCK
    dotdir_path = _get_dotgrail_dir(path)
    lock_path = dotdir_path / 'LOCK'

    # Don't sit there waiting for the Grailfile to be unlocked
    lock = fasteners.InterProcessLock(str(lock_path))
    with fasteners.try_lock(lock) as got:
        if not got:
            raise utils.GrailError("Grailfile is locked")

        # Open the manifest and read it entirely into memory
        lines = None
        with path.open('r') as f:
            lines = list(f.readlines())

        # Return the Grailfile object from the context manager
        grailfile = Grailfile(lines)
        yield grailfile

        # When the context manager is exiting, write out the contents of the manifest to disk.
        with path.open('w') as f:
            grailfile.write(f)

def _get_dotgrail_dir(path):
    dotgrail_path = path.parent / '.grail'
    dotgrail_path.mkdir(exist_ok=True)
    return dotgrail_path

@contextlib.contextmanager
def find():
    """Search up from the current directory for a Grailfile."""
    try:
        grailfile_dir = next(filter(_grailfile_exists, _search_path()))
        with _open_grailfile(grailfile_dir / 'Grailfile') as grailfile:
            yield grailfile
    except StopIteration as exc:
        raise utils.GrailError("No Grailfile found") from exc

class Grailfile:
    """Represents a Grailfile (a Grail manifest)."""
    def __init__(self, original_lines):
        self.data = {}
        for line in original_lines:
            package, version = map(str.strip, line.split('='))
            self.data[package] = version

    def add_pkg(self, pkgname):
        """Add a package@version to the manifest."""
        package, version = utils.parse_pkgname(pkgname)
        self.data[package] = version

    def rm_pkg(self, pkgname):
        """Remove a package from the manifest."""
        package, _ = utils.parse_pkgname(pkgname)
        del self.data[package]

    def write(self, f):
        """Write out the manifest to disk."""
        for k in sorted(self.data.keys()):
            f.write('{} = {}\n'.format(k, self.data[k]))

def _grailfile_exists(path):
    """Check whether or not a Grailfile exists in the given directory."""
    grailfile = path / 'Grailfile'
    return grailfile.exists() and not grailfile.is_dir()

def _search_path():
    """Return the current directory and all of its direct ancestors."""
    yield Path.cwd()
    yield from Path.cwd().parents
