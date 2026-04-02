"""
Shared SQLAlchemy helpers for model definitions.
"""

from __future__ import annotations

import enum

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON


JSONType = JSONB().with_variant(JSON(), "sqlite")


def enum_type(enum_cls: type[enum.Enum], *, name: str, **kwargs) -> Enum:
    """Consistently build Enum columns using enum values."""
    return Enum(
        enum_cls,
        name=name,
        values_callable=lambda enum_cls_: [member.value for member in enum_cls_],
        validate_strings=True,
        **kwargs,
    )


__all__ = ["JSONType", "enum_type"]