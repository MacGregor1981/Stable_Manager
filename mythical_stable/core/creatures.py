from abc import ABC, abstractmethod


class Creature(ABC):
    _total_creatures = 0

    def __init__(self, name: str, species: str, origin: str, power_level: int):
        self.name = name
        self.species = species
        self.__origin = origin
        self._power_level = power_level
        self._in_stable = True
        Creature._total_creatures += 1

    @classmethod
    def from_dict(cls, data: dict) -> Creature:
        allowed = ("name", "species", "origin", "power_level")
        dataf = {k: v for k, v in data.items() if k in allowed}
        return cls(**dataf)

    @classmethod
    def from_str(cls, data: str) -> Creature:
        datas = data.split(",")
        return cls(datas[0], datas[1], datas[2], datas[3])

    @property
    def power_level(self) -> int:
        return self._power_level

    @power_level.setter
    def power_level(self, power_level: float) -> None:
        if power_level < 0 or power_level > 100:
            raise ValueError("Power level out of range (0-100)")
        self._power_level = power_level

    @property
    def origin(self) -> str:
        return self.__origin

    @property
    def in_stable(self) -> bool:
        return self._in_stable

    @abstractmethod
    def mission_duration_days(self) -> int: ...

    @abstractmethod
    def describe_abilities(self) -> str: ...

    def send_on_mission(self) -> None:
        self._in_stable = False

    def return_to_stable(self) -> None:
        self._in_stable = True

    def get_total_creatures(self) -> int:
        return self._total_creatures

    def __str__(self) -> str:
        status = "in stable" if self._in_stable else "on mission"
        return f"{self.name} the {self.species} (origin: {self.__origin})[{status}]"

    def __repr__(self) -> str:
        return f"Creature(name={self.name!r}, species={self.species!r}, origin={self.__origin!r}, power_level={self._power_level!r})"

    @staticmethod
    def is_valid_species(species: str) -> bool:
        return species in [
            "Dragon",
            "Ice Dragon",
            "Phoenix",
            "Griffin",
            "Unicorn",
            "Basilisk",
        ]


class Dragon(Creature):

    def __init__(self, name, origin, power_level, element):
        super().__init__(name, "Dragon", origin, power_level)
        self.element = element

    def mission_duration_days(self) -> int:
        return 14

    def describe_abilities(self):
        return f"{self.name} breathes fire and flies at great speed"

    def __str__(self):
        status = "in stable" if self._in_stable else "on mission"
        return f"{self.name} the {self.species} [{self.element}] (origin: {self.__origin})[{status}]"


class Phoenix(Creature):

    __resurrection_count: int = 0

    def __init__(self, name, origin, power_level):
        super().__init__(name, "Phoenix", origin, power_level)

    def mission_duration_days(self) -> int:
        return 7

    def describe_abilities(self):
        return f"{self.name} can resurrect and has flame aura"

    def resurrect(self) -> None:
        self.__resurrection_count += 1
        print("resurrected!")


class Unicorn(Creature):

    def __init__(self, name, origin, power_level):
        super().__init__(name, "Unicorn", origin, power_level)

    def mission_duration_days(self) -> int:
        return 3

    def describe_abilities(self):
        return f"{self.name} can heal and goes fast"

    def send_on_mission(self):
        if self._power_level < 50:
            raise RuntimeError("A weak unicorn cannot be sent alone")
        return super().send_on_mission()
