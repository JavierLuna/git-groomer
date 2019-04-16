import datetime

import pytest

from git_groomer.base.objects import Commit, Branch


@pytest.fixture
def mock_commit():
    return Commit(long_id='b2ed8f2b119f0ee35e6e1c4e07ab5b4585998666', author='test@test.com', title='test',
                  message='test',
                  created_on=datetime.datetime.now(), parent_ids=['ee2c7ac'])


@pytest.fixture
def mock_branch(mock_commit):
    return Branch(name='test', merged=True, last_commit=mock_commit)


@pytest.fixture
def mock_git_client():
    return type('MockedGitClient', (), {'get_branches': []})


def test_commit_short_id(mock_commit):
    assert mock_commit.long_id.startswith(mock_commit.short_id)


def test_commit_short_id_in_str(mock_commit):
    assert mock_commit.short_id in str(mock_commit)


def test_commit_title_in_str(mock_commit):
    assert mock_commit.title in str(mock_commit)


def test_commit_author_in_str(mock_commit):
    assert mock_commit.author in str(mock_commit)


def test_commit_short_id_in_repr(mock_commit):
    assert mock_commit.short_id in repr(mock_commit)


def test_commit_title_in_repr(mock_commit):
    assert mock_commit.title in repr(mock_commit)


def test_commit_author_in_repr(mock_commit):
    assert mock_commit.author in repr(mock_commit)


def test_branch_name_is_str(mock_branch):
    assert mock_branch.name == str(mock_branch)


def test_branch_name_in_repr(mock_branch):
    assert mock_branch.name in repr(mock_branch)
