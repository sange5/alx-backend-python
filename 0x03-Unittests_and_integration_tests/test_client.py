#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.

Tests include:
- Organization retrieval (`org`)
- License checking (`has_license`)
- Public repositories (`public_repos`)
- Public repositories filtered by license (`public_repos_with_license`)
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for GithubOrgClient class.
    """

    @patch('client.GithubOrgClient.get_json')  # Mocking the get_json method
    def test_org(self, mock_get_json):
        """
        Test the org method of GithubOrgClient.
        """
        mock_get_json.return_value = {"login": "google", "id": 1234}
        client = GithubOrgClient("google")
        org_data = client.org()
        self.assertEqual(org_data, {"login": "google", "id": 1234})
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test the has_license method of GithubOrgClient.
        """
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @patch('client.GithubOrgClient.get_json')
    @patch('client.GithubOrgClient._public_repos_url', 
           new_callable=property)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient.
        """
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        client = GithubOrgClient("google")
        repos = client.public_repos()

        self.assertEqual(repos, ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

    def test_public_repos_with_license(self):
        """
        Test the public_repos method when filtering by license.
        """
        client = GithubOrgClient("google")
        with patch.object(client, "public_repos", return_value=[
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}}
        ]):
            repos_with_license = client.public_repos_with_license(
                "my_license")
            self.assertEqual(repos_with_license, ["repo1"])

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos_url(self, mock_get_json):
        """
        Test the _public_repos_url method of GithubOrgClient.
        """
        mock_get_json.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        client = GithubOrgClient("google")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")


if __name__ == '__main__':
    unittest.main()
