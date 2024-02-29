from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime
from .base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    location: Mapped[str] = mapped_column(String(255))
    attendees_count: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column(String(255))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("User", back_populates="events")
