from dataclasses import dataclass


@dataclass
class DatabaseObject:
    """Base class for all database objects."""

    name: str

    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # This is kept here for potential future use and because DatabaseObjectWithColumns calls it
        pass


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
