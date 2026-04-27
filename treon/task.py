import logging
import textwrap

from nbconvert.preprocessors import CellExecutionError
from nbconvert.utils.exceptions import ConversionException

from .test_execution import execute_notebook

LOG = logging.getLogger("treon.task")


def _is_verbose():
    return LOG.isEnabledFor(logging.DEBUG)


class Task:
    def __init__(self, file_path):
        self.file_path = file_path
        self.is_successful = False

    def run_tests(self):
        pass

    def result_string(self):
        pass

    def error_string(self, stack_trace):
        pass
