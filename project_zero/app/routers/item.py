from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/", response_model = List[schemas.PostOut])
def get_items(db: Session = Depends(get_db),
              current_user: models.Users = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    items = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    return items


@router.get("/sqlalchemy", response_model=List[schemas.Post])
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).group_by(models.Post.id).all()
    
    return {"data": posts}


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create(body: schemas.ItemBase, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **body.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"message": new_post}


@router.get("/{item_id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: Session = Depends(get_db)):
    
    item = db.query(models.Post).filter(models.Post.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found")
   
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, 
                db: Session = Depends(get_db), 
                current_user: models.Users = Depends(oauth2.get_current_user)):
    
    delete_query = db.query(models.Post).filter(models.Post.id == item_id)
    
    delete_post = delete_query.first()

    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found")
   

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this item")
        
    db.delete(delete_post)
    
    db.commit()
    
    return {"message": "Item deleted successfully", 
            "detail": delete_post}
@router.put("/{item_id}", response_model=schemas.Post, status_code=status.HTTP_202_ACCEPTED)
def update_item(item_id: int, item: schemas.Post,
                db: Session = Depends(get_db), 
                current_user: models.Users = Depends(oauth2.get_current_user)):
    
    update_post = db.query(models.Post).filter(models.Post.id == item_id)


    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Item not found")
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorized to delete this item")
    
    update_post.update(item.dict())
    db.commit()
    return update_post