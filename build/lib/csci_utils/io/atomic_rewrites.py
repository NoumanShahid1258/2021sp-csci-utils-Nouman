import os

from contextlib import contextmanager
from atomicwrites import atomic_write as _backend_writer, AtomicWriter


class SuffixWriter(AtomicWriter):
    def get_fileobject(self, suffix="", dir=None, **kwargs):
        return super().get_fileobject(suffix, dir, **kwargs)


@contextmanager
def atomic_write(file, mode="w", as_file=True, **kwargs):
    if os.path.exists(file):
        raise FileExistsError  # if file already exist

    f_name, extension = os.path.splitext(file)  # capture file name and extension

    with _backend_writer(
        file, writer_cls=SuffixWriter, mode=mode, suffix=extension, **kwargs
    ) as f:
        if as_file:
            yield f
        else:
            yield f.name
