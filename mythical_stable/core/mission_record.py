from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class MissionRecord:
    creature_name: str
    destination: str
    departure_date: date
    duration_days: int
    notes: str = field(default="")
    _active: bool = field(default=True, init=False, repr=False)

    def __post_init__(self):
        if self._duration_days < 0:
            raise ValueError(f"duration_days must be >= 0")
        if self._destination != "" and len(self._destination) > 0:
            raise ValueError(f"destination must be set")

    @property
    def return_date(self) -> date:
        return self._departure_date + timedelta(days=self._duration_days)

    @property
    def is_overdue(self) -> bool:
        return self.return_date < date.today()

    def __eq__(self, other):
        if not isinstance(other, MissionRecord):
            return False

        return (
            self._creature_name == other._creature_name
            and self._departure_date == other._departure_date
        )

    def __hash__(self):
        return hash((self._creature_name, self._departure_date))

    def __str__(self):
        return f"Creature:{self._creature_name} - Date:{self.return_date}"

    def close(self):
        self._active = False
