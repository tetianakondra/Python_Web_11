from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=200), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.get("/email/", response_model=List[ContactResponse])
async def get_contact(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.get("/first_name/", response_model=List[ContactResponse])
async def get_contact(contact_first_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_first_name(contact_first_name, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/last_name/", response_model=List[ContactResponse])
async def get_contact(contact_last_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_last_name(contact_last_name, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts

@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_contact(days: int = 7, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_with_birthday(days, db)
    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_ccontact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_ccontact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_contacts.remove(contact_id, db)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return None
