import unittest

from pyunitreport import HTMLTestRunner

if __name__ == "__main__":
    test_suit = unittest.defaultTestLoader.discover('cases/wap', pattern='test_*.py')
    test_runner = HTMLTestRunner(output='reports')
    test_results = test_runner.run(test_suit)
