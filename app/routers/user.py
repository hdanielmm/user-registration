from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from database.db_config import get_db
from models import user as models

from database.schemas import User, UserCreate
from utils import get_password_hash


router = APIRouter(prefix="/users", tags=["user"])

class Error404(Exception):
    pass


def error_404(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found",
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    print("Creating user:", user.dict())
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
):
    try:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()

        if user is None:
            raise Error404()

        user_query.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_200_OK)
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)


