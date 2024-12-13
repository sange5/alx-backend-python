import unittest
from parameterized import parameterized

# Define the access_nested_map function here for testing purposes.
def access_nested_map(nested_map, path):
    """Access a nested dictionary using a tuple of keys."""
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(f"Key '{key}' not found in the nested map.")
        current = current[key]
    return current

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ("simple_key", {"a": 1}, ("a",), 1),
        ("nested_key_level1", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_key_level2", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key_level1", {}, ("a",), "Key 'a' not found in the nested map."),
        ("missing_key_level2", {"a": 1}, ("a", "b"), "Key 'b' not found in the nested map."),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, expected_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)

if __name__ == "__main__":
    unittest.main()
