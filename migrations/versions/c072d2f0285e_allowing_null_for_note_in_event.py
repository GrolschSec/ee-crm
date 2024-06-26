"""allowing null for note in event

Revision ID: c072d2f0285e
Revises: d6ca774d2a9e
Create Date: 2024-04-09 08:10:08.999773

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c072d2f0285e"
down_revision: Union[str, None] = "d6ca774d2a9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "events", "notes", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "events", "notes", existing_type=sa.VARCHAR(length=255), nullable=False
    )
    # ### end Alembic commands ###
