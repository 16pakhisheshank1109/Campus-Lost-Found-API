from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select
from .models import Item
from .schemas import ItemCreate, ItemUpdate
from .database import create_db_and_table, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(
    title="Campus Lost & Found API",
    version="1.0.0",
    lifespan=lifespan,
)


def get_item_or_404(item_id: int, session: Session) -> Item:
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, session: Session = Depends(get_session)):
    item = Item.model_validate(data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items", response_model=list[Item])
def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()


@app.get("/items/status/{item_status}", response_model=list[Item])
def get_items_by_status(
    item_status: str,
    session: Session = Depends(get_session),
):
    if item_status not in {"Lost", "Found", "Returned"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be Lost, Found, or Returned",
        )

    statement = select(Item).where(Item.status == item_status)
    return session.exec(statement).all()


@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(
    category: str,
    session: Session = Depends(get_session),
):
    statement = select(Item).where(Item.category == category)
    return session.exec(statement).all()


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, session: Session = Depends(get_session)):
    return get_item_or_404(item_id, session)


@app.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    data: ItemUpdate,
    session: Session = Depends(get_session),
):
    item = get_item_or_404(item_id, session)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = get_item_or_404(item_id, session)
    session.delete(item)
    session.commit()