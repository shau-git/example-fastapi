"""add content column to posts table

Revision ID: ecea36f66dca
Revises: b75244009a7b
Create Date: 2024-09-08 21:05:44.737916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecea36f66dca'
down_revision: Union[str, None] = 'b75244009a7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
