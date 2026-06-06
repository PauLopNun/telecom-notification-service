class DomainError(Exception):
    """Base exception for domain-specific failures."""


class NotificationNotFoundError(DomainError):
    """Raised when a notification cannot be found."""


class InvalidNotificationDataError(DomainError):
    """Raised when notification data violates domain rules."""
