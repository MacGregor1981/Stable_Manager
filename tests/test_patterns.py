from __future__ import annotations

from unittest.mock import Mock

import pytest

from mythical_stable.patterns.commands import (
    CommandHistory,
    DispatchCommand,
)
from mythical_stable.patterns.observers import EventBus
from mythical_stable.patterns.strategies import (
    SortByAvailability,
    SortByName,
    SortByPower,
)

# ──────────────────────────────────────────────────────────────────────────────
# Test helpers
# ──────────────────────────────────────────────────────────────────────────────


class DummyCreature:
    def __init__(self, name: str, power_level: int, in_stable: bool = True):
        self.name = name
        self.power_level = power_level
        self._in_stable = in_stable


class DummyStable:
    def __init__(self, creatures):
        self.creatures = list(creatures)

    def sorted(self, strategy):
        return strategy.sort(self.creatures)


# ──────────────────────────────────────────────────────────────────────────────
# Strategy pattern tests
# ──────────────────────────────────────────────────────────────────────────────


def test_sort_by_name_returns_alphabetical_order():
    creatures = [
        DummyCreature("Zephyr", 50),
        DummyCreature("Aurora", 70),
        DummyCreature("Blaze", 60),
    ]

    strategy = SortByName()

    result = strategy.sort(creatures)

    assert [c.name for c in result] == ["Aurora", "Blaze", "Zephyr"]


def test_sort_by_power_returns_highest_power_first():
    creatures = [
        DummyCreature("Goblin", 10),
        DummyCreature("Dragon", 100),
        DummyCreature("Phoenix", 75),
    ]

    strategy = SortByPower()

    result = strategy.sort(creatures)

    assert [c.name for c in result] == ["Dragon", "Phoenix", "Goblin"]


def test_sort_by_availability_returns_in_stable_first():
    creatures = [
        DummyCreature("Hydra", 80, in_stable=False),
        DummyCreature("Basilisk", 60, in_stable=True),
        DummyCreature("Chimera", 70, in_stable=False),
        DummyCreature("Dragon", 100, in_stable=True),
    ]

    strategy = SortByAvailability()

    result = strategy.sort(creatures)

    assert [c.name for c in result] == [
        "Basilisk",
        "Dragon",
        "Chimera",
        "Hydra",
    ]


def test_stable_sorted_returns_new_list_and_does_not_modify_stable():
    creatures = [
        DummyCreature("Zephyr", 50),
        DummyCreature("Aurora", 70),
    ]

    stable = DummyStable(creatures)

    result = stable.sorted(SortByName())

    # Returned list is sorted
    assert [c.name for c in result] == ["Aurora", "Zephyr"]

    # Original stable order unchanged
    assert [c.name for c in stable.creatures] == ["Zephyr", "Aurora"]

    # Ensure a new list object is returned
    assert result is not stable.creatures


# ──────────────────────────────────────────────────────────────────────────────
# EventBus tests
# ──────────────────────────────────────────────────────────────────────────────


def test_listener_is_called_when_event_is_published():
    bus = EventBus()

    listener = Mock()

    bus.subscribe("mission_complete", listener)

    payload = {"name": "Phoenix"}

    bus.publish("mission_complete", payload)

    listener.assert_called_once_with(payload)


def test_listener_for_other_event_is_not_called():
    bus = EventBus()

    listener = Mock()

    bus.subscribe("event_x", listener)

    bus.publish("event_y", {"data": 123})

    listener.assert_not_called()


def test_multiple_listeners_on_same_event_are_all_called():
    bus = EventBus()

    listener_one = Mock()
    listener_two = Mock()

    bus.subscribe("mission", listener_one)
    bus.subscribe("mission", listener_two)

    payload = {"creature": "Dragon"}

    bus.publish("mission", payload)

    listener_one.assert_called_once_with(payload)
    listener_two.assert_called_once_with(payload)


def test_publishing_event_with_no_listeners_does_not_raise():
    bus = EventBus()

    bus.publish("unheard_event", {"value": 1})


# ──────────────────────────────────────────────────────────────────────────────
# Command / CommandHistory tests
# ──────────────────────────────────────────────────────────────────────────────


def test_dispatch_command_execute_dispatches_creature():
    service = Mock()

    cmd = DispatchCommand(
        service=service,
        name="Dragon",
        destination="Volcano",
        days=7,
    )

    cmd.execute()

    service.dispatch.assert_called_once_with("Dragon", "Volcano", 7)


def test_dispatch_command_undo_recalls_creature():
    service = Mock()

    cmd = DispatchCommand(
        service=service,
        name="Dragon",
        destination="Volcano",
        days=7,
    )

    cmd.undo()

    service.recall.assert_called_once_with("Dragon")


def test_command_history_undo_last_reverses_most_recent_command():
    service = Mock()

    history = CommandHistory()

    cmd = DispatchCommand(
        service=service,
        name="Phoenix",
        destination="Sky Temple",
        days=3,
    )

    history.execute(cmd)

    history.undo_last()

    service.dispatch.assert_called_once_with(
        "Phoenix",
        "Sky Temple",
        3,
    )
    service.recall.assert_called_once_with("Phoenix")


def test_command_history_undo_last_on_empty_history_raises_index_error():
    history = CommandHistory()

    with pytest.raises(IndexError, match="Nothing to undo"):
        history.undo_last()
