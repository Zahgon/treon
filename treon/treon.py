# pylint: disable=line-too-long
"""
Usage:
  treon
  treon [PATH]... [--threads=<number>] [-v] [--exclude=<string>]...

Arguments:
  PATH                File or directory path to find notebooks to test. Searches recursively for directory paths. [default: current working directory]

Options:
  --threads=<number>  Number of parallel threads. Each thread processes one notebook file at a time. [default: 10]
  -e=<string> --exclude=<string>  Option for excluding files or entire directories from testing. All files whose
                      absolute path starts with the specified string are excluded from testing. This option can be
                      specified more than once to exclude multiple files or directories. If the exclude path is
                      a valid directory name, only this directory is excluded.
  -v --verbose        Print detailed output for debugging.
  -h --help           Show this screen.
  --version           Show version.

"""

__version__ = "0.1.4"


import sys
import os
import glob
import logging
import textwrap
from multiprocessing.dummy import Pool as ThreadPool
from docopt import docopt, DocoptExit

from .task import Task

DEFAULT_THREAD_COUNT = 10

LOG = logging.getLogger("treon")


def main():
    try:
        arguments = docopt(__doc__, version=__version__)
    except DocoptExit:
        sys.exit(__doc__)

    setup_logging(arguments)
    LOG.info("Executing treon version %s", __version__)
    thread_count = arguments["--threads"] or DEFAULT_THREAD_COUNT
    notebooks = get_notebooks_to_test(arguments)
    tasks = [Task(notebook) for notebook in notebooks]
    print_test_collection(notebooks)
    trigger_tasks(tasks, thread_count)
    has_failed = print_test_result(tasks)

    if has_failed:
        sys.exit(-1)


def setup_logging(arguments):
    logging.basicConfig(format="%(message)s")
    LOG.setLevel(loglevel(arguments))


def loglevel(arguments):
    verbose = arguments["--verbose"]
    return logging.DEBUG if verbose else logging.INFO


def trigger_tasks(tasks, thread_count):
    pool = ThreadPool(int(thread_count))
    pool.map(Task.run_tests, tasks)


def print_test_result(tasks):
    has_failed = False
    succeeded = [t.file_path for t in tasks if t.is_successful]
    failed = [t.file_path for t in tasks if not t.is_successful]
    variables = {
        "succeeded_count": len(succeeded),
        "failed_count": len(failed),
        "total": len(tasks),
    }

    message = textwrap.dedent("""
              -----------------------------------------------------------------------
              TEST RESULT
              -----------------------------------------------------------------------\n""")

    if succeeded:
        message += "       -- PASSED \n".join(succeeded) + "       -- PASSED \n"

    if failed:
        has_failed = True
        message += "       -- FAILED \n".join(failed) + "       -- FAILED \n"

    message += (
        "-----------------------------------------------------------------------\n"
    )
    message += "{succeeded_count} succeeded, {failed_count} failed, out of {total} notebooks tested.\n".format(
        **variables
    )
    message += (
        "-----------------------------------------------------------------------\n"
    )
    LOG.info(message)
    return has_failed


def print_test_collection(notebooks):
    message = textwrap.dedent("""
              -----------------------------------------------------------------------
              Collected following Notebooks for testing
              -----------------------------------------------------------------------\n""")
    message += "\n".join(notebooks) + "\n"
    message += (
        "-----------------------------------------------------------------------\n"
    )
    LOG.debug(message)


def filter_results(results, args):
    pass


def get_notebooks_to_test(args):
    pass
