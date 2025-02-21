from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    age: int


from typing import List
from fastapi import FastAPI, HTTPException

users: List[User] = []

app = FastAPI()


@app.get("/users", response_model=List[User])
async def get_users():
    return users


from pydantic import Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Enter Username"),
    age: int = Field(
        ...,
        gt=0,
        le=150,
        description="Enter Age")


@app.post("/users", response_model=User)
async def create_user(user: UserCreate) -> User:    # переменная user, по которой FastAPI создает объект класса UserCreate
    if any(u.username == user.username for u in users): # или альтернативно: if user.username in [u.username for u in users]:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

#   Class User:
# Описывает модель данных для ответа API (например, когда вы возвращаете данные пользователя).
# Содержит поле id, которое генерируется на сервере.
#   UserCreate:
# Описывает модель данных для запроса на создание пользователя.
# Не содержит поле id, так как оно генерируется на сервере.
# Добавляет дополнительные ограничения (валидацию) для полей, например, min_length для username и gt/le для age.
#   Это разделение логично, так как:
# Данные, которые приходят от клиента (в запросе), могут отличаться от данных, которые возвращаются клиенту (в ответе).
# Валидация для входящих данных (UserCreate) может быть более строгой, чем для исходящих данных (User).

# if any(u.username == user.username for u in users): и if user.username in users): не равнозначны в данном контексте.
# Давайте разберем, почему:
# if any(u.username == user.username for u in users):
# Эта строка проверяет, существует ли в списке users хотя бы один пользователь (u), у которого поле username совпадает
# с user.username. Это корректный способ проверки уникальности имени пользователя в вашем коде.
# if user.username in users):
# Эта строка пытается проверить, содержится ли user.username в списке users. Однако это не будет работать,
# так как users — это список объектов типа User, а не список строк (username). Python не сможет автоматически сравнить
# строку (user.username) с объектами User в списке, и это вызовет ошибку

# Когда использовать Pydantic модели (class UserCreate(BaseModel):), а когда Annotated с Path/Query?
# Использование Pydantic моделей (как UserCreate) и Annotated с Path/Query не являются равнозначными —
# они решают разные задачи и применяются в разных сценариях:
#   Если /user/{username}/{age}
# Если функция ожидает username и age в пути URL, а не в теле запроса, то Pydantic модель для тела запроса не нужна.
# Вместо этого используйте Annotated с Path и обрабатывает его через user: UserCreate.
#   Когда использовать Pydantic модели?
# Если данные приходят в теле запроса (например, JSON), используйте Pydantic модель.
# Например, в исходном коде create_user ожидает JSON вида:
#   Комбинирование подходов
# Можно одновременно использовать параметры пути и тело запроса. Например, если username передается в пути, а
# остальные данные — в теле:
# @app.post("/user/{username}", response_model=User)
# async def create_user(
#     username: Annotated[str, Path(...)],
#     user_data: UserCreate  # Данные из тела запроса (кроме username)
# ):
#   Правильно я понимаю, что я задаю переменную user, которая имеет атрибуты класса UserCreate?
# В вашем коде переменная user — это объект класса UserCreate, который создается автоматически FastAPI на основе данных,
# переданных в теле запроса (например, JSON). Этот объект имеет атрибуты класса UserCreate, такие как username и age.

from typing import Annotated
from fastapi import Path


@app.post("/users/{username}/{age}", response_model=User)
async def create_user_(
        username: Annotated[
            str,
            Path(
                min_length=5,
                max_length=100,
                description="Enter Username"
            )
        ],
        age: Annotated[
            int,
            Path(
                gt=0,
                le=150,
                description="Enter Age"
            )
        ]
):
    if any(u.username == username for u in users): # или альтернативно: if user.username in [u.username for u in users]:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/users/{user_id}/{username}/{age}', response_model=User)
async def update_user(
        user_id: Annotated[
            int,
            Path(
                description="Enter user_id"
            )
        ],
        username: Annotated[
            str,
            Path(
                min_length=3,
                max_length=20,
                regex="^[a-zA-Z0-9_-]+$",
                description="Enter username"
            )
        ],
        age: int
):
    if users:
        for user in users:
            if user.id == user_id:  # в моей модели User полу называется id, а не user_id
                user.username = username  # user[username] не правильно, так как не словарь, а объект и
                # 'username' не правильно, тогда жестко задаю именно 'username', а надо передать параметр username
                user.age = age
                return user
        else:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    raise HTTPException(status_code=404, detail="Список пустой")

# Логика с else внутри цикла - else должен быть на уровне for - всех проверить и только если нет, выбросить исключение
# Вызов raise HTTPException внутри цикла с else приведет к тому, что исключение будет выброшено при первой же неудачной
# попытке найти пользователя. Это неправильно, так как нужно проверить всех пользователей.

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i) # или del users[i] - удаление по индексу
            return {"detail": f"Пользователь {user_id} удален"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")

# Метод remove в списках Python удаляет элемент по значению, а не по индексу. Вы передаете i (индекс), но remove
# ожидает объект user. Это вызовет ошибку или некорректное поведение.
#   Логика удаления:
# Для удаления элемента по индексу нужно использовать метод del users[i] или users.pop(i).
