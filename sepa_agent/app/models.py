from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DirectDebit(Base):
    __tablename__ = "direct_debits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creditor_name = Column(String, index=True)
    creditor_iban = Column(String)
    debtor_name = Column(String)
    debtor_iban = Column(String)
    amount = Column(Float)
    channel_initiated = Column(String)
    account_number = Column(String)
    remittance_info = Column(String)
