from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import ItemCreate, ItemDB, ItemResponse, UserDB

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[ItemDB]:
    return db.query(ItemDB).offset(skip).limit(limit).all()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemDB:
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)) -> ItemDB:
    owner = db.query(UserDB).filter(UserDB.id == item_in.owner_id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    item = ItemDB(
        title=item_in.title,
        description=item_in.description,
        owner_id=item_in.owner_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_in: ItemCreate, db: Session = Depends(get_db)) -> ItemDB:
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item.title = item_in.title
    item.description = item_in.description
    item.owner_id = item_in.owner_id
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)
    db.commit()
