from this import d
from ... import models, schemas, utils, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/itineary",
    tags=['itineary']
)

# Normal customer create a new itineary 
@router.post("/new_itineary", status_code= status.HTTP_201_CREATED, response_model=schemas.LoansResponse) 
def create_loan(loan: schemas.LoansCreate, current_user: schemas.Customer = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    # **<classname>.dict will unpack all the contents of the json and put it into our model
    if current_user["role"]=="user":
        nloan = loan.dict()
        nloan["customer_id"]=current_user["id"]
        new_loan = models.Loan(**nloan) 
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan) #similar to RETURNINING in normal SQL
        return new_loan
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Only Normal users can use this")

# Normal customer gets all their loans
@router.get("/myloans", response_model=List[schemas.LoansResponse]) 
def get_all_loans_of_user(current_user: schemas.Customer = Depends(oauth2.get_current_user), db: Session = Depends(get_db), limit:int = 10, skip:int = 0):
    if current_user["role"]=="user":
        loans = db.query(models.Loan).filter(models.Loan.customer_id == current_user["id"]).limit(limit).offset(skip).all()
        return loans
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Only Normal users can use this")

# Admin user gets ALL loans
@router.get("/all_loans", response_model=List[schemas.LoansResponse]) 
def get_all_loans(current_user: schemas.Customer = Depends(oauth2.get_current_user), db: Session = Depends(get_db), limit:int = 10, skip:int = 0):
    
    if current_user["role"]=="admin":
        loans = db.query(models.Loan).limit(limit).offset(skip).all()
        return loans
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Only Admin users can use this")

# Admin user gets ALL loans of a customer
@router.get("/all_loans/customerid={customer_id}", response_model=List[schemas.LoansResponse]) 
def get_all_loans(customer_id:int, current_user: schemas.Customer = Depends(oauth2.get_current_user), db: Session = Depends(get_db), limit:int = 10, skip:int = 0):
    
    if current_user["role"]=="admin":
        loans = db.query(models.Loan).filter(models.Loan.customer_id==customer_id).limit(limit).offset(skip).all()
        return loans
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Only Admin users can use this")
