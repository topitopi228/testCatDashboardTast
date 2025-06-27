from core.models.base import Base
from sqlalchemy import Column, Date, Numeric, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.target import Target
    from core.models.spy_cat import Cat


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cat_id: Mapped[int] = mapped_column(Integer, ForeignKey("cats.id"))
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    cat: Mapped["Cat"] = relationship(back_populates="missions")
    targets: Mapped[list["Target"]] = relationship(back_populates="mission")
