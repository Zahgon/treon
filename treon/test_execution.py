import os
import textwrap
import nbformat

from nbformat.v4 import new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor


def execute_notebook(path):
    pass


def metadata(path):
    return {"metadata": {"path": os.path.dirname(path)}}


def parse_test_result(cells):
    pass


def parse_unittest_output(outputs):
    pass


def parse_doctest_output(outputs):
    pass


def unittest_cell():
    source = textwrap.dedent("""
        from IPython.display import clear_output
        import unittest

        r = unittest.main(argv=[''], verbosity=2, exit=False)

        if r.result.testsRun == 0:
            clear_output()
    """)
    return new_code_cell(source=source)


def doctest_cell():
    source = textwrap.dedent("""
        from IPython.display import clear_output
        import doctest

        r = doctest.testmod(verbose=True)

        if r.attempted == 0:
            clear_output()
    """)
    return new_code_cell(source=source)
