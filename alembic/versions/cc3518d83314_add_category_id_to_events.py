"""add category_id to events

Revision ID: cc3518d83314
Revises: 81ca6a15b920
Create Date: 2026-11-24 23:15:55.418218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc3518d83314'
down_revision: Union[str, Sequence[str], None] = '81ca6a15b920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add category_id temporarily as nullable
    op.add_column(
        'events',
        sa.Column('category_id', sa.Integer(), nullable=True)
    )

    # 2. Assign existing events to the Tech category (ID 3)
    op.execute(
        "UPDATE events SET category_id = 3"
    )

    # 3. Make category_id mandatory
    op.alter_column(
        'events',
        'category_id',
        existing_type=sa.Integer(),
        nullable=False
    )

    # 4. Create the foreign-key constraint
    op.create_foreign_key(
        'fk_events_category_id_categories',
        'events',
        'categories',
        ['category_id'],
        ['id'],
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_events_category_id_categories',
        'events',
        type_='foreignkey'
    )

    op.drop_column('events', 'category_id')

