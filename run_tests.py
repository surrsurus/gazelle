import sys
sys.dont_write_bytecode = True

from tests import testsuite
testsuite.integration_tests()