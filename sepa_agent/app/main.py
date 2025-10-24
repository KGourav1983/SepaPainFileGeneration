from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# SQLite Database URL
DATABASE_URL = "sqlite:///./test.db"

# Create a SQLAlchemy engine for SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define the DirectDebit model for the database
class DirectDebit(Base):
    __tablename__ = "direct_debits"
    id = Column(Integer, primary_key=True, index=True)
    creditor_name = Column(String, index=True)
    creditor_iban = Column(String)
    debtor_name = Column(String)
    debtor_iban = Column(String)
    amount = Column(Float)
    channel_initiated = Column(String)
    account_number = Column(String)
    remittance_info = Column(String)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic model to validate incoming requests
class DirectDebitRequest(BaseModel):
    creditor_name: str
    creditor_iban: str
    debtor_name: str
    debtor_iban: str
    amount: float
    channel_initiated: str
    account_number: str
    remittance_info: str

# API endpoint to accept a Direct Debit request
@app.post("/direct-debit/")
def create_direct_debit(request: DirectDebitRequest):
    db = SessionLocal()
    db_debit = DirectDebit(**request.dict())
    db.add(db_debit)
    db.commit()
    db.refresh(db_debit)
    db.close()
    return {"message": "Direct Debit Request Accepted"}

# API endpoint to get all stored transactions
@app.get("/direct-debit/", response_model=List[DirectDebitRequest])
def get_all_debits():
    db = SessionLocal()
    debits = db.query(DirectDebit).all()
    db.close()
    return debits

# Function to generate the Pain File
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from app import models, schemas

def generate_pain_file(db: Session, file_path: str):
    # Query all Direct Debit transactions from the database
    transactions = db.query(models.DirectDebit).all()

    # Start XML structure
    root = ET.Element("Document")
    pain = ET.SubElement(root, "CstmrDrctDbtInitn")

    # Add the header info, e.g., Group Header (GrpHdr)
    grp_hdr = ET.SubElement(pain, "GrpHdr")
    ET.SubElement(grp_hdr, "MsgId").text = "MSG123456789"  # Example Message ID
    ET.SubElement(grp_hdr, "CreDtTm").text = "2025-10-24T10:30:00"  # Example Date/Time
    ET.SubElement(grp_hdr, "NbOfTxs").text = str(len(transactions))  # Number of transactions

    # Iterate over the transactions to generate individual Payment Information (PmtInf)
    for txn in transactions:
        pmt_info = ET.SubElement(pain, "PmtInf")
        ET.SubElement(pmt_info, "PmtInfId").text = f"PMT{txn.id}"
        ET.SubElement(pmt_info, "Amt").text = str(txn.amount)  # Amount to debit
        ET.SubElement(pmt_info, "Dbtr").text = txn.debtor_name  # Debtor Name
        ET.SubElement(pmt_info, "DbtrIBAN").text = txn.debtor_iban  # Debtor IBAN
        ET.SubElement(pmt_info, "Cdtr").text = txn.creditor_name  # Creditor Name
        ET.SubElement(pmt_info, "CdtrIBAN").text = txn.creditor_iban  # Creditor IBAN
        ET.SubElement(pmt_info, "RmtInf").text = txn.remittance_info  # Remittance Info

    # Create the ElementTree and write it to a file
    tree = ET.ElementTree(root)
    tree.write(file_path)

    return f"PAIN file generated at {file_path}"
