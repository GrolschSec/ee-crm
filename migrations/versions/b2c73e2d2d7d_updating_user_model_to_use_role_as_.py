"""updating user model to use role as property rather than a relationship

Revision ID: b2c73e2d2d7d
Revises: df9d296887d0
Create Date: 2024-04-04 12:01:55.406660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c73e2d2d7d"
down_revision: Union[str, None] = "df9d296887d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
