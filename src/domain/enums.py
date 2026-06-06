from enum import StrEnum


class EventType(StrEnum):
    NETWORK_OUTAGE = "NETWORK_OUTAGE"
    SERVICE_DEGRADATION = "SERVICE_DEGRADATION"
    MAINTENANCE = "MAINTENANCE"
    BILLING_ALERT = "BILLING_ALERT"
    SECURITY_ALERT = "SECURITY_ALERT"


class NotificationStatus(StrEnum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    ACKNOWLEDGED = "ACKNOWLEDGED"


class DomainEventName(StrEnum):
    NOTIFICATION_CREATED = "notification.created"
    NOTIFICATION_STATUS_UPDATED = "notification.status_updated"
    NOTIFICATION_DELETED = "notification.deleted"
