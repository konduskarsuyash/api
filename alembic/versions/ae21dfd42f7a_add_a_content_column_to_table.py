"""add a content column to table

Revision ID: ae21dfd42f7a
Revises: fe49a0d08fdc
Create Date: 2024-10-27 08:52:20.863761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae21dfd42f7a'
down_revision: Union[str, None] = 'fe49a0d08fdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=True))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
