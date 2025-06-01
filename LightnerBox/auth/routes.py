
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from LightnerBox.database import get_db
from .. import models
from LightnerBox.models import User
from LightnerBox.schemas import UserCreate, UserLogin
from .utils import hash_password, verify_password
from .jwt_handler import create_access_token
# از JWT یوزر رو درمیاره
from ..auth.dependencies import get_current_user
from typing import List
from datetime import datetime, UTC
from ..models import Card, User
from ..schemas import CardCreate, CardUpdate, Card as CardSchema

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user.email == User.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user.email == User.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username})

    return {"msg": "Login successful", "access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"username": current_user.username}


@router.post("/cards", response_model=CardSchema)
def create_card(card: CardCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_card = Card(
        **card.model_dump(),
        user_id=user.id,
        box=1,
        next_due_date=datetime.now(UTC)
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get("/cards/", response_model=List[CardSchema])
def read_cards(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Card).filter(user.id == Card.user_id).all()


@router.get("/cards/{card_id}", response_model=CardSchema)
def get_card(card_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    card = db.query(Card).filter_by(id=card_id, user_id=user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/cards/{card_id}", response_model=CardSchema)
def update_card(card_id: int, updated: CardUpdate, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    card = db.query(Card).filter_by(id=card_id, user_id=user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(card, key, value)
        db.commit()
        db.refresh(card)
        return card


@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    card = db.query(Card).filter_by(id=card_id, user_id=user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}
