from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260606_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

EVENT_TYPE_VALUES = (
    "NETWORK_OUTAGE",
    "SERVICE_DEGRADATION",
    "MAINTENANCE",
    "BILLING_ALERT",
    "SECURITY_ALERT",
)
STATUS_VALUES = ("PENDING", "SENT", "FAILED", "ACKNOWLEDGED")


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("client_id", sa.String(length=100), nullable=False),
        sa.Column(
            "event_type",
            _enum_column("notification_event_type", EVENT_TYPE_VALUES),
        ),
        sa.Column("status", _enum_column("notification_status", STATUS_VALUES)),
        sa.Column("message", sa.String(length=1000), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notifications_client_id", "notifications", ["client_id"])


def downgrade() -> None:
    op.drop_index("ix_notifications_client_id", table_name="notifications")
    op.drop_table("notifications")


def _enum_column(name: str, values: tuple[str, ...]) -> sa.Enum:
    return sa.Enum(*values, name=name, native_enum=False, length=50)
