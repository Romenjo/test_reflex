"""empty message

Revision ID: cdd348b19a9c
Revises: 55317eca99a7
Create Date: 2024-11-24 17:17:25.812842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'cdd348b19a9c'
down_revision: Union[str, None] = '55317eca99a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_statistics')
    op.drop_table('competitions')
    op.drop_table('games')
    op.drop_table('player_valuations')
    op.drop_table('competition_rounds')
    op.drop_table('positions')
    op.drop_table('seasons')
    op.drop_table('countries')
    op.drop_table('players')
    op.drop_table('clubs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('club_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('domestic_competition_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['domestic_competition_id'], ['competitions.competition_id'], name='clubs_domestic_competition_id_fkey'),
    sa.PrimaryKeyConstraint('club_id', name='clubs_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('players',
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('foot', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('height_in_cm', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('nationality_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('current_club_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('market_value_in_eur', sa.NUMERIC(precision=15, scale=2), autoincrement=False, nullable=True),
    sa.Column('position_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['current_club_id'], ['clubs.club_id'], name='players_current_club_id_fkey'),
    sa.ForeignKeyConstraint(['nationality_id'], ['countries.country_id'], name='players_nationality_id_fkey'),
    sa.ForeignKeyConstraint(['position_id'], ['positions.position_id'], name='players_position_id_fkey'),
    sa.PrimaryKeyConstraint('player_id', name='players_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('countries',
    sa.Column('country_id', sa.INTEGER(), server_default=sa.text("nextval('countries_country_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('country_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('country_id', name='countries_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('seasons',
    sa.Column('season_start_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('season_end_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('season_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('season_id', name='seasons_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('positions',
    sa.Column('position_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('position_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('sub_position_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('position_id', name='positions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('competition_rounds',
    sa.Column('cr_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('competition_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('round_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.competition_id'], name='competition_rounds_competition_id_fkey'),
    sa.PrimaryKeyConstraint('cr_id', name='competition_rounds_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('player_valuations',
    sa.Column('valuation_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('market_value_in_eur', sa.NUMERIC(precision=15, scale=2), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.player_id'], name='player_valuations_player_id_fkey'),
    sa.PrimaryKeyConstraint('valuation_id', name='player_valuations_pkey')
    )
    op.create_table('games',
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('season_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('home_club_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('away_club_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('home_club_goals', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('away_club_goals', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('winner_club_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cr_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['away_club_id'], ['clubs.club_id'], name='games_away_club_id_fkey'),
    sa.ForeignKeyConstraint(['cr_id'], ['competition_rounds.cr_id'], name='games_cr_id_fkey'),
    sa.ForeignKeyConstraint(['home_club_id'], ['clubs.club_id'], name='games_home_club_id_fkey'),
    sa.ForeignKeyConstraint(['season_id'], ['seasons.season_id'], name='games_season_id_fkey'),
    sa.ForeignKeyConstraint(['winner_club_id'], ['clubs.club_id'], name='games_winner_club_id_fkey'),
    sa.PrimaryKeyConstraint('game_id', name='games_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('competitions',
    sa.Column('competition_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('type', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('country_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.country_id'], name='competitions_country_id_fkey'),
    sa.PrimaryKeyConstraint('competition_id', name='competitions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('player_statistics',
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('season_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('goals', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('assists', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('yellow_cards', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('red_cards', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('minutes_played', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('rating', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], name='player_statistics_game_id_fkey'),
    sa.ForeignKeyConstraint(['player_id'], ['players.player_id'], name='player_statistics_player_id_fkey'),
    sa.ForeignKeyConstraint(['season_id'], ['seasons.season_id'], name='player_statistics_season_id_fkey'),
    sa.PrimaryKeyConstraint('player_id', 'game_id', 'season_id', name='player_statistics_pkey')
    )
    # ### end Alembic commands ###