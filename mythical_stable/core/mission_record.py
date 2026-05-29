from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class MissionRecord:
    creature_name: str
    destination: str
    departure_date: date
    duration_days: int
    notes: str = field(default="")
    active: bool = field(default=True, init=False, repr=False)

    def __post_init__(self):
        if self.duration_days < 0:
            raise ValueError(f"duration_days must be >= 0")
        if self.destination == "" or len(self.destination) <= 0:
            raise ValueError(f"destination must be set")

    @property
    def return_date(self) -> date:
        return self.departure_date + timedelta(days=self.duration_days)

    @property
    def is_overdue(self) -> bool:
        return self.return_date < date.today()

    def __eq__(self, other):
        if not isinstance(other, MissionRecord):
            return False

        return (
            self.creature_name == other.creature_name
            and self.departure_date == other.departure_date
        )

    def __hash__(self):
        return hash((self.creature_name, self.departure_date))

    def __str__(self):
        return f"Creature:{self.creature_name} - Date:{self.return_date}"

    def close(self):
        self.active = False
