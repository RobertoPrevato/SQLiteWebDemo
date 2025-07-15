"""
This module defines the database model with entities and their properties.
Code-first approach is used to generate migrations using Alembic.

These objects are defined according to the domain model, which is simpler and abstracted
from SQL.

If you wish to edit an Record, modify first a class here, then create a migration.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata = mapper_registry.metadata

Base = mapper_registry.generate_base()


class FortuneCookieRecord(Base):  # type: ignore
    """A fortune cookie."""

    __tablename__ = "cookies"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
