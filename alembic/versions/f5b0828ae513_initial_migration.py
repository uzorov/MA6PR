"""initial migration

Revision ID: f5b0828ae513
Revises: 
Create Date: 2023-12-07 15:02:51.328073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f5b0828ae513'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('books',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('author', sa.String(), nullable=False),
                    sa.Column('genre', sa.String(), nullable=False),
                    sa.Column('publisher', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('books')
