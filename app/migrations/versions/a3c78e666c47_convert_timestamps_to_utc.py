"""convert timestamps to UTC

Revision ID: a3c78e666c47
Revises: 8d5af4676d1a
Create Date: 2025-12-03 19:45:48.317103

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a3c78e666c47"
down_revision: Union[str, Sequence[str], None] = "8d5af4676d1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Convert existing naive Madrid timestamps to UTC."""
    op.execute(
        """
        UPDATE dht11reading
        SET timestamp = (timestamp AT TIME ZONE 'Europe/Madrid') AT TIME ZONE 'UTC'
        WHERE timestamp IS NOT NULL;
    """
    )


def downgrade() -> None:
    """Optional: convert UTC back to Madrid local time."""
    op.execute(
        """
        UPDATE dht11reading
        SET timestamp = (timestamp AT TIME ZONE 'UTC') AT TIME ZONE 'Europe/Madrid'
        WHERE timestamp IS NOT NULL;
    """
    )
