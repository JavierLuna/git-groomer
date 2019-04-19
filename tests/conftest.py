import freezegun
import maya
import pytest


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
