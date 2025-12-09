"""make timestamps timezone aware

Revision ID: d67b8e4e3bed
Revises: a3c78e666c47
Create Date: 2025-12-03 20:02:49.939744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d67b8e4e3bed"
down_revision: Union[str, Sequence[str], None] = "a3c78e666c47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "dht11reading",
        "timestamp",
        type_=sa.DateTime(timezone=True),
        postgresql_using="timestamp AT TIME ZONE 'UTC'",
    )


def downgrade():
    op.alter_column(
        "dht11reading",
        "timestamp",
        type_=sa.DateTime(timezone=False),
        postgresql_using="timestamp AT TIME ZONE 'UTC'",
    )
