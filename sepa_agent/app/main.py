from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models, schemas  # Import models and schemas
import xml.etree.ElementTree as ET
import os
from .models import Base  # Import Base from models.py
from .schemas import DirectDebitRequest
from .models import DirectDebit  # Import DirectDebit from models.py

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# SQLite Database URL
DATABASE_URL = "sqlite:///./test.db"


# Create a SQLAlchemy engine for SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# In main.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the SEPA PAIN File Generation API"}


# API endpoint to accept a Direct Debit request
@app.post("/direct-debit/")
def create_direct_debit(request: DirectDebitRequest, db: Session = Depends(get_db)):
    try:
        db_debit = models.DirectDebit(**request.dict())
        db.add(db_debit)
        db.commit()
        db.refresh(db_debit)
        return {"message": "Direct Debit Request Accepted", "data": request.dict()}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}



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

# Call to generate the Pain File


router = APIRouter()

@router.get("/generate-pain-file/")
def generate_pain_file_endpoint(db: Session = Depends(get_db)):
    file_path = "/path/to/your/storage/sepa_pain.xml"  # Define the location where you want to store the file
    result = generate_pain_file(db, file_path)
    return {"message": result}


