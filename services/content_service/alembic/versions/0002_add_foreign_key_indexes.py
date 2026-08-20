"""add indexes on foreign key columns

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-19
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_contents_owner_id", "contents", ["owner_id"])
    op.create_index("ix_generation_history_content_id", "generation_history", ["content_id"])
    op.create_index("ix_audio_assets_content_id", "audio_assets", ["content_id"])


def downgrade() -> None:
    op.drop_index("ix_audio_assets_content_id", table_name="audio_assets")
    op.drop_index("ix_generation_history_content_id", table_name="generation_history")
    op.drop_index("ix_contents_owner_id", table_name="contents")
