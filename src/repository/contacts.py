from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import ContactModel
from src.database.models import Contact


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      contact_number=body.contact_number,
                      birthday=body.birthday,
                      additional_information=body.additional_information
                      )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.contact_number = body.contact_number
        contact.birthday = body.birthday
        contact.additional_information = body.additional_information
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

# Пошук контакту за ім'ям
async def find_contact_by_first_name(contact_first_name: str, db: Session) -> List[Contact]:
    contact = db.query(Contact).filter(Contact.first_name == contact_first_name).all()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    else:
        return contact

# Пошук контакту за прізвищем
async def find_contact_by_last_name(contact_last_name: str, db: Session) -> List[Contact]:
    contact = db.query(Contact).filter(Contact.last_name == contact_last_name).all()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    else:
        return contact

# Пошук контакту за адресою електронної пошти
async def find_contact_by_email(contact_email: str, db: Session) -> List[Contact]:
    contact = db.query(Contact).filter(Contact.email == contact_email).all()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    else:
        return contact

async def upcoming_birthdays(current_date, to_date, skip: int, limit: int, db: Session) -> List[Contact]:
    contacts = db.query(Contact).offset(skip).limit(limit).all()

    upcoming = []

    # Пошук в контактах по дням народження
    for contact in contacts:

        contact_birthday = (contact.birthday.month, contact.birthday.day)
        current_date = (current_date.month, current_date.day)
        to_date = (to_date.month, to_date.day)

        if current_date < contact_birthday <= to_date:
            upcoming.append(contact)

    return upcoming