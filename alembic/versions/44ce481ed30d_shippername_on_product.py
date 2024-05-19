"""shippername on product

Revision ID: 44ce481ed30d
Revises: 7062b9a39d22
Create Date: 2024-05-18 12:14:22.148340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44ce481ed30d'
down_revision: Union[str, None] = '7062b9a39d22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product', sa.Column('shippername', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('product','shippername')
