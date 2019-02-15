# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Index, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, LONGTEXT, MEDIUMINT, SMALLINT, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'account'

    username = Column(VARCHAR(32), primary_key=True)
    password = Column(VARCHAR(32), nullable=False)
    first_warning_timestamp = Column(INTEGER(11))
    failed_timestamp = Column(INTEGER(11))
    failed = Column(VARCHAR(32))
    level = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    last_encounter_lat = Column(Float(18, True))
    last_encounter_lon = Column(Float(18, True))
    last_encounter_time = Column(INTEGER(11))
    spins = Column(SMALLINT(6), nullable=False, server_default=text("'0'"))


class Group(Base):
    __tablename__ = 'group'

    name = Column(VARCHAR(32), primary_key=True)
    perm_view_map = Column(TINYINT(1), nullable=False)
    perm_view_map_raid = Column(TINYINT(1), nullable=False)
    perm_view_map_pokemon = Column(TINYINT(1), nullable=False)
    perm_view_stats = Column(TINYINT(1), nullable=False)
    perm_admin = Column(TINYINT(1), nullable=False)
    perm_view_map_gym = Column(TINYINT(1), nullable=False)
    perm_view_map_pokestop = Column(TINYINT(1), nullable=False)
    perm_view_map_spawnpoint = Column(TINYINT(1), nullable=False)
    perm_view_map_quest = Column(TINYINT(1), nullable=False)
    perm_view_map_iv = Column(TINYINT(1), nullable=False)
    perm_view_map_cell = Column(TINYINT(1), nullable=False)


class Instance(Base):
    __tablename__ = 'instance'

    name = Column(VARCHAR(30), primary_key=True)
    type = Column(ENUM('circle_pokemon', 'circle_raid', 'circle_smart_raid', 'auto_quest', 'pokemon_iv'), nullable=False)
    data = Column(LONGTEXT, nullable=False)


class Metadatum(Base):
    __tablename__ = 'metadata'

    key = Column(VARCHAR(200), primary_key=True)
    value = Column(TEXT)


class PokemonStat(Base):
    __tablename__ = 'pokemon_stats'

    date = Column(Date, primary_key=True, nullable=False)
    pokemon_id = Column(SMALLINT(6), primary_key=True, nullable=False)
    count = Column(INTEGER(11), nullable=False)


class QuestStat(Base):
    __tablename__ = 'quest_stats'

    date = Column(Date, primary_key=True, nullable=False)
    reward_type = Column(SMALLINT(6), primary_key=True, nullable=False, server_default=text("'0'"))
    pokemon_id = Column(SMALLINT(6), primary_key=True, nullable=False, server_default=text("'0'"))
    item_id = Column(SMALLINT(6), primary_key=True, nullable=False, server_default=text("'0'"))
    count = Column(INTEGER(11), nullable=False)


class RaidStat(Base):
    __tablename__ = 'raid_stats'

    date = Column(Date, primary_key=True, nullable=False)
    pokemon_id = Column(SMALLINT(6), primary_key=True, nullable=False)
    count = Column(INTEGER(11), nullable=False)
    level = Column(SMALLINT(3))


class S2cell(Base):
    __tablename__ = 's2cell'
    __table_args__ = (
        Index('ix_coords', 'center_lat', 'center_lon'),
    )

    id = Column(BIGINT(20), primary_key=True)
    level = Column(TINYINT(3))
    center_lat = Column(Float(18, True), nullable=False, server_default=text("'0.00000000000000'"))
    center_lon = Column(Float(18, True), nullable=False, server_default=text("'0.00000000000000'"))
    updated = Column(INTEGER(11), nullable=False, index=True)


class Spawnpoint(Base):
    __tablename__ = 'spawnpoint'
    __table_args__ = (
        Index('ix_coords', 'lat', 'lon'),
    )

    id = Column(BIGINT(15), primary_key=True)
    lat = Column(Float(18, True), nullable=False)
    lon = Column(Float(18, True), nullable=False)
    updated = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))
    despawn_sec = Column(SMALLINT(6))


class WebSession(Base):
    __tablename__ = 'web_session'

    token = Column(VARCHAR(255), primary_key=True)
    userid = Column(VARCHAR(255))
    created = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    updated = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    idle = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    data = Column(TEXT)
    ipaddress = Column(VARCHAR(255))
    useragent = Column(TEXT)


class Device(Base):
    __tablename__ = 'device'

    uuid = Column(VARCHAR(40), primary_key=True)
    instance_name = Column(ForeignKey('instance.name', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    last_host = Column(VARCHAR(30))
    last_seen = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    account_username = Column(ForeignKey('account.username', ondelete='SET NULL', onupdate='CASCADE'), unique=True)

    account = relationship('Account')
    instance = relationship('Instance')


class Gym(Base):
    __tablename__ = 'gym'
    __table_args__ = (
        Index('ix_coords', 'lat', 'lon'),
    )

    id = Column(VARCHAR(35), primary_key=True)
    lat = Column(Float(18, True), nullable=False)
    lon = Column(Float(18, True), nullable=False)
    name = Column(VARCHAR(128))
    url = Column(VARCHAR(200))
    last_modified_timestamp = Column(INTEGER(11))
    raid_end_timestamp = Column(INTEGER(11), index=True)
    raid_spawn_timestamp = Column(INTEGER(11))
    raid_battle_timestamp = Column(INTEGER(11))
    updated = Column(INTEGER(11), nullable=False, index=True)
    raid_pokemon_id = Column(SMALLINT(6), index=True)
    guarding_pokemon_id = Column(SMALLINT(6))
    availble_slots = Column(SMALLINT(6))
    team_id = Column(TINYINT(3))
    raid_level = Column(TINYINT(3))
    enabled = Column(TINYINT(1))
    ex_raid_eligible = Column(TINYINT(1))
    in_battle = Column(TINYINT(1))
    raid_pokemon_move_1 = Column(SMALLINT(6))
    raid_pokemon_move_2 = Column(SMALLINT(6))
    raid_pokemon_form = Column(TINYINT(3))
    raid_pokemon_cp = Column(SMALLINT(6))
    raid_is_exclusive = Column(TINYINT(1))
    cell_id = Column(ForeignKey('s2cell.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    cell = relationship('S2cell')


class Pokestop(Base):
    __tablename__ = 'pokestop'
    __table_args__ = (
        Index('ix_coords', 'lat', 'lon'),
    )

    id = Column(VARCHAR(35), primary_key=True)
    lat = Column(Float(18, True), nullable=False)
    lon = Column(Float(18, True), nullable=False)
    name = Column(VARCHAR(128))
    url = Column(VARCHAR(200))
    lure_expire_timestamp = Column(INTEGER(11), index=True)
    last_modified_timestamp = Column(INTEGER(11))
    updated = Column(INTEGER(11), nullable=False, index=True)
    enabled = Column(TINYINT(1))
    quest_type = Column(INTEGER(11))
    quest_timestamp = Column(INTEGER(11))
    quest_target = Column(SMALLINT(6))
    quest_conditions = Column(TEXT)
    quest_rewards = Column(TEXT)
    quest_template = Column(VARCHAR(100))
    quest_pokemon_id = Column(SMALLINT(6), index=True)
    quest_reward_type = Column(SMALLINT(6), index=True)
    quest_item_id = Column(SMALLINT(6), index=True)
    cell_id = Column(ForeignKey('s2cell.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    cell = relationship('S2cell')


class User(Base):
    __tablename__ = 'user'

    username = Column(VARCHAR(32), primary_key=True)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(72), nullable=False)
    discord_id = Column(BIGINT(20), index=True)
    email_verified = Column(TINYINT(1), server_default=text("'0'"))
    group_name = Column(ForeignKey('group.name', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'default'"))

    group = relationship('Group')


class Assignment(Base):
    __tablename__ = 'assignment'

    device_uuid = Column(ForeignKey('device.uuid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    instance_name = Column(ForeignKey('instance.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    time = Column(MEDIUMINT(6), primary_key=True, nullable=False)

    device = relationship('Device')
    instance = relationship('Instance')


class Pokemon(Base):
    __tablename__ = 'pokemon'
    __table_args__ = (
        Index('ix_coords', 'lat', 'lon'),
    )

    id = Column(VARCHAR(25), primary_key=True)
    pokestop_id = Column(ForeignKey('pokestop.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    spawn_id = Column(ForeignKey('spawnpoint.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    lat = Column(Float(18, True), nullable=False)
    lon = Column(Float(18, True), nullable=False)
    weight = Column(Float(18, True))
    size = Column(Float(18, True))
    expire_timestamp = Column(INTEGER(11), index=True)
    updated = Column(INTEGER(11), index=True)
    pokemon_id = Column(SMALLINT(6), nullable=False, index=True)
    move_1 = Column(SMALLINT(6))
    move_2 = Column(SMALLINT(6))
    gender = Column(TINYINT(3))
    cp = Column(SMALLINT(6))
    atk_iv = Column(TINYINT(3), index=True)
    def_iv = Column(TINYINT(3), index=True)
    sta_iv = Column(TINYINT(3), index=True)
    form = Column(TINYINT(3))
    level = Column(TINYINT(3), index=True)
    weather = Column(TINYINT(3))
    costume = Column(TINYINT(3))
    first_seen_timestamp = Column(INTEGER(11), nullable=False)
    changed = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))
    iv = Column(Float(5), index=True)
    cell_id = Column(ForeignKey('s2cell.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    expire_timestamp_verified = Column(TINYINT(1), nullable=False)

    cell = relationship('S2cell')
    pokestop = relationship('Pokestop')
    spawn = relationship('Spawnpoint')


class Token(Base):
    __tablename__ = 'token'

    token = Column(VARCHAR(50), primary_key=True)
    type = Column(ENUM('confirm_email', 'reset_password'), nullable=False)
    username = Column(ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    expire_timestamp = Column(INTEGER(11), nullable=False, index=True)

    user = relationship('User')
