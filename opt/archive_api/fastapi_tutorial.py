from typing import Annotated, Any
from fastapi import FastAPI, Query, Path, Body
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from pydantic import EmailStr

from db.smitdb import SmitDb
from db.schemas import AuthenticationSchema

from authentication.auth_api import AuthApi


def create_db_and_tables():
    """
    Creates the database and necessary tables for the authentication module.
    """
    SmitDb(AuthenticationSchema).create_table()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the lifespan of the FastAPI app.
    """
    
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}/items/{item_id}")
async def read_item_id(item_id: int,
                       user_id: int,
                       q: str | None = None,
                       short : bool = False,
                       ):
    item: dict[str, Any] = {'item_id' : item_id, 'user_id' : user_id}
    if q:
        item.update({'q' : q })
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get('/items/')
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


### validation
class Item(SQLModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very  Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.post('/items')
def create_item(item: Item) -> Item:
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item

@app.put('/items/{item_id}')
async def update_item(
    item_id: Annotated[int, Path(title="Id from path parameter", ge=0, le=1000)], 
    importance: Annotated[int, Body(gt=6)],
    item: Annotated[Item, None],
    q: str | None = None,
    ):
    result: dict[str, Any] = {'item_id' : item_id}
    if q:
        result.update({'q' : q})
    if item:
        result.update({'item' : item})
    return result

@app.get('/items/')
async def read_items(q: Annotated[str | None, 
                                  Query(min_length=3,
                                        max_length=50, 
                                        pattern='^fixedquery$')] = None):
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


class UserIn(SQLModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(SQLModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
            return user


######################################################
# @app.get("/users/")
# async def read_users():
#     return AuthApi().read_all_users()


# @app.get("/users/{username}")
# async def read_user(username: str):
#     try:
#         return AuthApi().get_user(username)
#     except Exception as e:
#         return e

@app.post("/users/", response_model=AuthenticationSchema)
async def create_user(user: AuthenticationSchema):
    #try:
    SmitDb(AuthenticationSchema).create_instance(user)

    return user
    # except Exception as e:
    #     return e
    #AuthApi().write_user(user)