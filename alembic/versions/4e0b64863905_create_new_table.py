"""create new table

Revision ID: 4e0b64863905
Revises: 023af95d25d6
Create Date: 2026-11-16 15:34:31.849455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e0b64863905'
down_revision: Union[str, Sequence[str], None] = '023af95d25d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column('id', sa.Integer(),nullable=False,primary_key=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','id')
