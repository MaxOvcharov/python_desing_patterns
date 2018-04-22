#!/usr/bin/env python3
"""
Example from - https://github.com/azmikamis/pipbook/blob/master/any/Unpack.py
"""

import gzip
import errno
import os
import re
import shutil
import string
import tarfile
import tempfile
import zipfile


class Archive:

    def __init__(self, filename):
        self._names = None
        self._unpack = None
        self._file = None
        self.filename = filename

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, name):
        self.close()
        self.__filename = name

    def close(self):
        if self._file is not None:
            self._file.close()
        self._names = self._unpack = self._file = None

    def names(self):
        if self._file is None:
            self._prepare()
        return self._names()

    def unpack(self):
        if self._file is None:
            self._prepare()
        self._unpack()

    def _prepare(self):
        if self.filename.endswith((".tar.gz", ".tar.bz2", ".tar.xz", ".zip")):
            self._prepare_tarball_or_zip()
        elif self.filename.endswith(".gz"):
            self._prepare_gzip()
        else:
            raise ValueError(f'unreadable: {self.filename}')

    def _prepare_tarball_or_zip(self):

        def safe_extractall():
            unsafe = []
            for name in self.names():
                if not self.is_safe(name):
                    unsafe.append(name)
            if unsafe:
                raise ValueError(f'unsafe to unpack: {unsafe}')
            self._file.extractall()

        if self.filename.endswith(".zip"):
            self._file = zipfile.ZipFile(self.filename)
            self._names = self._file.namelist
            self._unpack = safe_extractall
        else: # Ends with .tar.gz, .tar.bz2, or .tar.xz
            suffix = os.path.splitext(self.filename)[1]
            self._file = tarfile.open(self.filename, "r:" + suffix[1:])
            self._names = self._file.getnames
            self._unpack = safe_extractall

    def _prepare_gzip(self):
        self._file = gzip.open(self.filename)
        filename = self.filename[:-3]
        self._names = lambda: [filename]

        def extractall():
            with open(filename, "wb") as f:
                f.write(self._file.read())

        self._unpack = extractall

    @staticmethod
    def is_safe(filename):
        return not (filename.startswith(("/", "\\")) or
                    (len(filename) > 1 and filename[1] == ":" and
                     filename[0] in string.ascii_letter) or
                    re.search(r"[.][.][/\\]", filename))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __str__(self):
        return f'{self.filename}({self._file is not None})'


def zip_file_exp(to_path):
    zip_filename = os.path.join(to_path, "test.zip")
    zip_names = ["Bag1.py", "Bag2.py", "Bag3.py"]
    file = None
    try:
        file = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED)
        for name in zip_names:
            file.write(name)
    finally:
        if file is not None:
            file.close()

    return zip_filename, zip_names


def tar_file_exp(to_path):
    tar_filename = os.path.join(to_path, "test.tar.gz")
    tar_names = ["genome1.py", "genome2.py", "genome3.py"]
    file = None
    try:
        file = tarfile.open(tar_filename, "w:gz")
        for name in tar_names:
            file.add(name)
    finally:
        if file is not None:
            file.close()

    return tar_filename, tar_names


def gzip_file_exp(to_path):
    gz_filename = os.path.join(to_path, "hello.pyw.gz")
    gz_name = "hello.pyw"
    file = None
    try:
        file = gzip.open(gz_filename, "w")
        with open(gz_name, "rb") as infile:
            file.write(infile.read())
    finally:
        if file is not None:
            file.close()

    return gz_filename, gz_name


def main():
    """
    This code is designed to work with 3.1+, so can't use
      os.makedirs()'s exist_ok keyword argument, can't use
      zipfile.ZipFile as a context manager, and can't use
      text mode for gzip.
    """
    to_path = os.path.join(tempfile.gettempdir(), "unpack")
    try:
        os.makedirs(to_path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

    zip_filename, zip_names = zip_file_exp(to_path)
    tar_filename, tar_names = tar_file_exp(to_path)
    gz_filename, gz_name = gzip_file_exp(to_path)

    os.chdir(to_path)
    with Archive(zip_filename) as archive:
        print(archive.names())
        assert archive.names() == zip_names
        archive.unpack()

        archive.filename = tar_filename
        print(archive.names())
        assert archive.names() == tar_names
        archive.unpack()

        archive.filename = gz_filename
        archive.unpack()

    shutil.rmtree(to_path)


if __name__ == "__main__":
    main()
