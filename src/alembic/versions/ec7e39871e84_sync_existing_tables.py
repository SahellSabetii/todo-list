"""sync_existing_tables

Revision ID: ec7e39871e84
Revises: 73eb4af62e7a
Create Date: 2025-11-28 01:19:08.544268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec7e39871e84'
down_revision: Union[str, Sequence[str], None] = '73eb4af62e7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
