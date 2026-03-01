#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------
# INFO:
# -----------------------------------------------------------------------------------------------------------------------

"""
Author: OpenCode
License: Apache 2.0
Description: Test Coconut terminal and warning behavior.
"""

# -----------------------------------------------------------------------------------------------------------------------
# IMPORTS:
# -----------------------------------------------------------------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

from coconut.root import *  # NOQA

import sys
import unittest

if sys.version_info < (2, 7):
    from StringIO import StringIO
else:
    from io import StringIO

from coconut.command.cli import arguments
from coconut.exceptions import CoconutException
from coconut.terminal import Logger


# -----------------------------------------------------------------------------------------------------------------------
# TESTS:
# -----------------------------------------------------------------------------------------------------------------------


class TestTerminal(unittest.TestCase):
    def test_cli_silence_warnings_arg(self):
        parsed_args = arguments.parse_args(["--silence-warnings", "ignore this"])
        assert parsed_args.silence_warnings == "ignore this"

    def test_silence_warning_regex(self):
        logger = Logger()
        logger.setup(silence_warnings="ignore this")

        old_stderr, sys.stderr = sys.stderr, StringIO()
        try:
            logger.warn("ignore this")
            ignored_output = sys.stderr.getvalue()

            logger.warn("keep this")
            warned_output = sys.stderr.getvalue()
        finally:
            sys.stderr = old_stderr

        assert ignored_output == ""
        assert "keep this" in warned_output

    def test_invalid_silence_warning_regex(self):
        with self.assertRaises(CoconutException):
            Logger().setup(silence_warnings="[")


if __name__ == "__main__":
    unittest.main()
