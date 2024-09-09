"""add last few column to posts table

Revision ID: 8008c9d99c43
Revises: 5bdbfafc6fe1
Create Date: 2024-09-08 21:59:32.167326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8008c9d99c43'
down_revision: Union[str, None] = '5bdbfafc6fe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))
                              
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
