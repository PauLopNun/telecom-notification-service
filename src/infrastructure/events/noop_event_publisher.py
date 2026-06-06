from src.domain.models.domain_event import DomainEvent
from src.domain.ports.event_publisher import EventPublisherPort


class NoOpEventPublisher(EventPublisherPort):
    async def publish_event(self, event: DomainEvent) -> None:
        return None
