"""adding event support contact can be null

Revision ID: d6ca774d2a9e
Revises: 82148928218f
Create Date: 2024-04-08 21:53:26.357387

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6ca774d2a9e"
down_revision: Union[str, None] = "82148928218f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "events", "support_contact_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "events", "support_contact_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###
