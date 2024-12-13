"""Added AWS and some other features

Revision ID: 5dc53ce7a8b2
Revises: 23a57ea787c5
Create Date: 2024-12-06 04:35:33.409362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5dc53ce7a8b2'
down_revision: Union[str, None] = '23a57ea787c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_index('ix_apscheduler_jobs_next_run_time', table_name='apscheduler_jobs')
    #op.drop_table('apscheduler_jobs')
    op.add_column('job_applications', sa.Column('comments', sa.Text(), nullable=True))
    op.add_column('job_applications', sa.Column('cv', sa.String(), nullable=True))
    op.add_column('job_applications', sa.Column('cover_letter', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_applications', 'cover_letter')
    op.drop_column('job_applications', 'cv')
    op.drop_column('job_applications', 'comments')
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='apscheduler_jobs_pkey')
    )
    op.create_index('ix_apscheduler_jobs_next_run_time', 'apscheduler_jobs', ['next_run_time'], unique=False)
    # ### end Alembic commands ###
