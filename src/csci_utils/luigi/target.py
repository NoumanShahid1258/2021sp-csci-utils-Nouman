import os
import io
import random

from contextlib import contextmanager

from luigi.local_target import LocalTarget, atomic_file
from luigi.format import FileWrapper


class suffix_preserving_atomic_file(atomic_file):
    # Reference: https://luigi.readthedocs.io/en/stable/_modules/luigi/local_target.html
    def generate_tmp_path(self, path):
        return path + "-luigi-tmp-%09d" % random.randrange(0, 1e10)

    def move_to_final_destination(self):
        os.rename(self.tmp_path, self.path)


class BaseAtomicProviderLocalTarget(LocalTarget):
    # Allow some composability of atomic handling
    atomic_provider = suffix_preserving_atomic_file

    def open(self, mode="r"):
        # leverage super() as well as modifying any code in LocalTarget
        # to use self.atomic_provider rather than atomic_file

        if mode == "r":
            _file = FileWrapper(io.BufferedReader(io.FileIO(self.path, mode)))
            return _file

        elif mode == "w":
            self.makedirs()
            return self.atomic_provider(self.path)

        else:
            raise Exception("Incorrect file mode (%s)" % mode)

    @contextmanager
    def temporary_path(self):
        # NB: unclear why LocalTarget doesn't use atomic_file in its implementation
        self.makedirs()
        with self.atomic_provider(self.path) as af:
            yield af.tmp_path


class SuffixPreservingLocalTarget(BaseAtomicProviderLocalTarget):
    atomic_provider = suffix_preserving_atomic_file
