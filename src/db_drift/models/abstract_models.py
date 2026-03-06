from dataclasses import dataclass


@dataclass
class DatabaseObject:
    """Base class for all database objects."""


@dataclass
class DatabaseObjectWithDoc(DatabaseObject):
    """Database object that can have documentation/comments."""

    doc: str


@dataclass
class DatabaseObjectWithHashedBody(DatabaseObject):
    """Database object with executable code (functions, procedures, etc.)."""

    body: str  # body is expected to be hashed
    definition: str  # definition may not be hashed


@dataclass
class DatabaseObjectWithDefinition(DatabaseObject):
    """Database object defined by a simple definition string."""

    definition: str


@dataclass
class DatabaseObjectWithDefinitionAndDoc(DatabaseObjectWithDefinition, DatabaseObjectWithDoc):
    """Database object that has both a definition and documentation."""
