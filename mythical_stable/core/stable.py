from typing import Iterator

from core.creatures import Creature


class Stable:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self) -> None:
        if hasattr(self, "_creatures"):
            return
        self._creatures: list[Creature] = []

    def add(self, creature: Creature) -> None:
        if creature.name in self:
            raise ValueError(
                f"A creature named '{creature.name}' is already registered."
            )
        self._creatures.append(creature)

    def remove(self, name: str) -> None:
        creature = self[name]
        self._creatures.remove(creature)

    def find(self, name: str) -> Creature:
        for creature in self._creatures:
            if creature.name == name:
                return creature
        raise KeyError(f"No creature named '{name}' in the stable.")

    def __len__(self) -> int:
        return len(self._creatures)

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, str):
            return False
        return any(c.name == name for c in self._creatures)

    def __iter__(self) -> Iterator[Creature]:
        return iter(self._creatures)

    def __getitem__(self, name: str) -> Creature:
        return self.find(name)

    def __repr__(self) -> str:
        names = [c.name for c in self._creatures]
        return f"Stable({len(self)} creatures: {names})"

    def available_by_power(self) -> StableIterator:
        return StableIterator(self._creatures)


class StableIterator:

    def __init__(self, creatures: list[Creature]) -> None:
        available = [c for c in creatures if c._in_stable]
        self._snapshot: list[Creature] = sorted(
            available, key=lambda c: c.power_level, reverse=True
        )
        self._index: int = 0

    def __iter__(self) -> StableIterator:
        return self

    def __next__(self) -> Creature:
        if self._index >= len(self._snapshot):
            raise StopIteration
        creature = self._snapshot[self._index]
        self._index += 1
        return creature
