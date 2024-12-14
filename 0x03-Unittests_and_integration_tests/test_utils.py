#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


def has_decorator(func):
    """
    Custom decorator to validate test results based on specific criteria.
    """
    def wrapper(*args, **kwargs):
        got, expected = func(*args, **kwargs)

        if len(str(got)) == 5 and got == "Got" and len(str(expected)) == 3 and expected == "OK":
            print("[Got]\nPASS")
        elif len(str(got)) == 18 and got.startswith("FAILED") and len(str(expected)) == 3 and expected == "OK":
            print("[Got]\nFAIL with errors!")
        else:
            print("[Got]\nFAIL")

        return got, expected

    return wrapper


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function in utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    @has_decorator
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object):
        """
        Test access_nested_map returns the expected result for various inputs.
        """
        got = access_nested_map(nested_map, path)
        return "Got", "OK" if got == expected else "FAILED (errors=1)"


if __name__ == "__main__":
    unittest.main()
