from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, Date, DateTime, ForeignKey
from datetime import date, datetime
from .base import Base

class Client(Base):
	__tablename__ = 'clients'

	id: Mapped[int] = mapped_column(primary_key=True)
	full_name: Mapped[str] = mapped_column(String(50))
	email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
	phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
	address: Mapped[str] = mapped_column(String(255))
	company_name: Mapped[str] = mapped_column(String(50))
	creation_date: Mapped[date] = mapped_column(Date, default=date.today())
	last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
	sales_contact_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

	sales_contact = relationship('User', back_populates='clients')
	contracts = relationship('Contract', back_populates='client')
