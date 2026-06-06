from abc import ABC, abstractmethod

from src.domain.models.domain_event import DomainEvent


class EventPublisherPort(ABC):
    """Publishes domain events to an external message broker."""

    @abstractmethod
    async def publish_event(self, event: DomainEvent) -> None:
        raise NotImplementedError
