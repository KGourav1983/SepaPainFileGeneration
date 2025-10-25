from pydantic import BaseModel
from typing import Optional

class DirectDebitRequest(BaseModel):
    creditor_name: str
    creditor_iban: str
    debtor_name: str
    debtor_iban: str
    amount: float
    channel_initiated: str
    account_number: str
    remittance_info: str

class DirectDebitRead(DirectDebitRequest):
    id: int  # include auto-generated ID

    class Config:
        orm_mode = True  # This tells Pydantic to treat the SQLAlchemy model as a Pydantic model
