from sqlalchemy import Column, Date, Numeric, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from core.models.base import Base
if TYPE_CHECKING:
    from core.models.mission import Mission

class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mission_id: Mapped[int] = mapped_column(Integer, ForeignKey("missions.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    mission: Mapped["Mission"] = relationship(back_populates="targets")