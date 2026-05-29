from abc import ABC, abstractmethod
from core.Creatures import Creature


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, creatures:list[Creature]) -> list[Creature]: ...

class SortByPower(SortStrategy):
    def sort(self, creatures:list[Creature]) -> list[Creature]:
        return sorted(creatures, key=lambda creature: creature.power_level, reverse=True)

class SortByName(SortStrategy):
    def sort(self, creatures:list[Creature]) -> list[Creature]:
        return sorted(creatures,key=lambda creature: creature.name)

class SortByAvailability(SortStrategy):
    def sort(self, creatures:list[Creature]) -> list[Creature]:
        """Return in-stable creatures before on-mission creatures."""
        return sorted(creatures, key=lambda c: (not c._in_stable, c.name))
        # creatures_in_stable = []
        # creature_in_mission = []
        # for creature in creatures:
        #     if creature.in_stable:
        #         creatures_in_stable.append(creature)
        #     else:
        #         creature_in_mission.append(creature)
        # full_list:lst[Creature] = []
        # full_list.extend(sorted(creatures_in_stable, key=lambda c: c.name))
        # full_list.extend(sorted(creature_in_mission, key=lambda c: c.name))
        # return fullList