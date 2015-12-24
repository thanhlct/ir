import sys
import pdb

class ForkedPdb(pdb.Pdb):
    """A Pdb subclass that may be used
    from a forked multiprocessing child

    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = file('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin

class ForkablePdb(pdb.Pdb):

    _original_stdin_fd = sys.stdin.fileno()
    _original_stdin = None

    def interaction(self, *args, **kwargs):
        if not self._original_stdin:
            self._original_stdin = os.fdopen(self._original_stdin_fd)
        current_stdin = sys.stdin
        try:
            sys.stdin = self._original_stdin
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = current_stdin
