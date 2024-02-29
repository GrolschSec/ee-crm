from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, Date
from datetime import date
from .base import Base

class Contract(Base):
	__tablename__ = 'contracts'

	id: Mapped[int] = mapped_column(primary_key=True)
	client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
	amount_total: Mapped[float] = mapped_column(Numeric(10, 2))
	amount_due: Mapped[float] = mapped_column(Numeric(10, 2))
	creation_date: Mapped[date] = mapped_column(Date, default=date.today())

	client = relationship('Client', back_populates='contracts')
	event = relationship('Event', back_populates='contract')