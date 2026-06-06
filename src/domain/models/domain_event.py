from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from src.domain.enums import DomainEventName


@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_name: DomainEventName
    aggregate_id: UUID
    payload: dict[str, Any]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
