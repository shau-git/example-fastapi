"""create posts table

Revision ID: b75244009a7b
Revises: 
Create Date: 2024-09-08 20:44:20.264931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

#because once you wanna edit the database have to delete the database, this approach can no need to delete entire database when updating col etc
# revision identifiers, used by Alembic.
revision: str = 'b75244009a7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:      #tablename ='posts'
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
