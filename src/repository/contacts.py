from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(contact_email: str, db: Session):
    contacts = db.query(Contact).filter(
        Contact.email.like(f"%{contact_email}%")).all()
    return contacts


async def get_contacts_by_first_name(contact_first_name: str, db: Session):
    contacts = db.query(Contact).filter(
        Contact.first_name.like(f"%{contact_first_name}%")).all()
    return contacts


async def get_contacts_by_last_name(contact_last_name: str, db: Session):
    contacts = db.query(Contact).filter(
        Contact.last_name.like(f"%{contact_last_name}%")).all()
    return contacts


async def get_contacts_with_birthday(days, db: Session):
    contacts = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        for i in range(days):
            celebration_day = datetime.now() + timedelta(days=i)
            if contact.birthday.day == celebration_day.day and contact.birthday.month == celebration_day.month:
                contacts.append(contact)
    return contacts


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
