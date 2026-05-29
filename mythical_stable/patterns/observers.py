class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, fn: Callable) -> None:
        self._listeners.setdefault(event, []).append(fn)

    def publish(self, event:str, payload) -> None:
        for fn in self._listeners.get(event, []):
            fn(payload)


# ── Built-in listener functions ───────────────────────────────────────────────

def audit_logger(payload) -> None:
    """Print a timestamped audit line for any event payload."""
    print(f"[AUDIT {datetime.now():%H:%M:%S}] {payload}")


def overdue_checker(record: "MissionRecord") -> None:
    """Warn if the recalled mission record was overdue."""
    if record.is_overdue:
        print(f"⚠️  OVERDUE: {record.creature_name} was due back on {record.return_date}")