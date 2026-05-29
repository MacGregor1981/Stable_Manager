import pytest
from mythical_stable.core import Dragon, Phoenix, Unicorn, Stable

@pytest.fixture
def frostbite():
    return Dragon("Frostbite", "Nordic Realms", 95, element="ice")

@pytest.fixture
def ember():
    return Phoenix("Ember", "Ashlands", 80)

@pytest.fixture
def stardust():
    return Unicorn("Stardust", "Silver Meadows", 72)

@pytest.fixture
def tinsel():
    return Unicorn("Tinsel", "Soft Glades", 30)

@pytest.fixture
def mission_frostbite():
    return MissionRecord(
        creature_name="Frostbite",
        destination="Stormwind",
        departure_date=date.today(),
        duration_days=2,
        notes="plop",
        active=True)

def mission_frostbite_equal():
    return MissionRecord(
        creature_name="Frostbite",
        destination="Unknow",
        departure_date=date.today(),
        duration_days=3,
        notes="Friday",
        active=false)

def mission_frostbite_not_overdue():
    return MissionRecord(
        creature_name = "Frostbite",
        destination = "Stormwind",
        departure_date = date.today() - timedelta(days=3),
        duration_days = 2,
        notes = "plop",
        active = True)

@pytest.fixture
def populated_stable(frostbite, ember, stardust):
    s = Stable()
    s.add(frostbite)
    s.add(ember)
    s.add(stardust)
    return s

@pytest.fixture
def gollum_name():
    return "Gollum"

@pytest.fixture
def stardust_name():
    return "Stardust"