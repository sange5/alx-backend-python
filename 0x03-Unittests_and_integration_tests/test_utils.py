#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function in utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """
        Test access_nested_map returns the expected result for various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in the nested map."),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in the nested map."),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_message: str) -> None:
        """
        Test access_nested_map raises KeyError with the expected message for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Debugging output for mismatches
        print(f"[Got] {str(context.exception)}")
        print(f"[Expected] {expected_message}")
        self.assertEqual(str(context.exception), expected_message)


if __name__ == "__main__":
    unittest.main()