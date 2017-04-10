from __future__ import absolute_import, print_function

import unittest
import logging

from .test_trees import TestSTrees
from .test_selectors import TestSelectors
from .test_parser import TestPlyPlus
from .test_grammars import TestPythonG, TestConfigG

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    unittest.main()
