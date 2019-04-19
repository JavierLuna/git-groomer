import pytest

from git_groomer.gitlab.client import GitlabClient


@pytest.fixture
def mock_gitlab_client():
    return GitlabClient(1, api_token='test')
