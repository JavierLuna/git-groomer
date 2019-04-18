from unittest.mock import Mock
import freezegun
import maya

import pytest

from git_groomer.base.objects import Commit, Branch, Repository


@pytest.fixture(scope="session", autouse=True)
def freeze_time(request):
    freezer = freezegun.freeze_time('2012-05-15')
    freezer.start()
    request.addfinalizer(lambda: freezer.stop())


@pytest.fixture
def today():
    return maya.now().datetime()


@pytest.fixture
def tomorrow(today):
    return today + maya.timedelta(days=1)


@pytest.fixture
def yesterday(today):
    return today - maya.timedelta(days=1)


@pytest.fixture
def mock_commit(yesterday):
    return Commit(long_id='b2ed8f2b119f0ee35e6e1c4e07ab5b4585998666', author='test@test.com', title='test',
                  message='test',
                  created_on=yesterday, parent_ids=['ee2c7ac'])


@pytest.fixture
def mock_branch(mock_commit):
    return Branch(name='test', merged=True, last_commit=mock_commit)


@pytest.fixture
def mock_git_client():
    return type('MockedGitClient', (), {'get_branches': Mock(return_value=[])})


@pytest.fixture
def mock_repository(mock_git_client):
    return Repository('test', mock_git_client)


@pytest.fixture
def mock_branch_pool(yesterday, today, tomorrow):
    return {'author': Branch('author', last_commit=Commit(author='test', created_on=today)),
            'older_than': Branch('older_than', last_commit=Commit(created_on=yesterday)),
            'newer_than': Branch('newer_than', last_commit=Commit(created_on=tomorrow)),
            'name_num': Branch('1', last_commit=Commit(created_on=today)),
            'name_string': Branch('test', last_commit=Commit(created_on=today)),
            'merged': Branch('merged', merged=True, last_commit=Commit(created_on=today)),
            'not_merged': Branch('not_merged', merged=True, last_commit=Commit(created_on=today))}
