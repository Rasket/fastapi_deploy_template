from logging.config import fileConfig
from typing import Iterable

from colorama import Fore
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic.operations import MigrationScript
from alembic.environment import MigrationContext

from sqlmodel import SQLModel
from alembic import context
from models import generate
import warnings
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

""" from os import environ
section = config.config_ini_section
config.set_section_option(section, "POSTGRES_USER", environ.get("POSTGRES_USER"))
config.set_section_option(section, "POSTGRES_PASSWORD", environ.get("POSTGRES_PASSWORD"))
config.set_section_option(section, "POSTGRES_DB", environ.get("POSTGRES_DB"))
config.set_section_option(section, "compose_db_name", environ.get("DB_HOST")) """

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    from sqlalchemy import create_engine
    import re
    import os

    url_tokens = {
        "DB_USER": os.getenv("POSTGRES_USER", ""),
        "DB_PASS": os.getenv("POSTGRES_PASSWORD", ""),
        "DB_HOST": os.getenv("compose_project_name_db", ""),
        "DB_NAME": os.getenv("POSTGRES_DB", "")
    }
    def process_revision_directives(
        context: MigrationContext,
        revision: str | Iterable[str | None] | Iterable[str],
        directives: list[MigrationScript],
    ):
        assert config.cmd_opts is not None
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            assert script.upgrade_ops is not None
            if script.upgrade_ops.is_empty():
                directives[:] = []
                warnings.warn(Fore.RED + 'EMPTY MIGRATION IS DETECTED, CONSIDERING MIGRATION AS NONE')

    url = config.get_main_option("sqlalchemy.url")

    url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
