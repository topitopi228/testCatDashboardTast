from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
import enum

from core.models.base import Base
from sqlalchemy import Column, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mission import Mission


class Breed(str, enum.Enum):
    ABYSSINIAN = "Abyssinian"
    BENGAL = "Bengal"
    SIAMESE = "Siamese"

class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[Breed] = mapped_column(ENUM(Breed), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)

    missions: Mapped[list["Mission"]] = relationship(back_populates="cat")