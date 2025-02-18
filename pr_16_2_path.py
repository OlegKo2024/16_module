from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()


@app.get('/user/{user_id}')
async def get_user(
        user_id: Annotated[
            int,
            Path(
                ge=1,
                le=100,
                description='Enter User ID',
                examples={
                    "min_value": {
                        "summary": "Минимальное значение",
                        "value": 1
                    },
                    "max_value": {
                        "summary": "Максимальное значение",
                        "value": 100
                    }
                }
            )
        ]
):
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user/{username}/{age}')  # http://127.0.0.1:8000/user/Oleg%20Ko/58
async def get_user(
        username: Annotated[
            str,
            Path(
                min_length=5,
                max_length=20,
                description='Enter username (длина от 5 до 20 символов, только буквы и пробелы)',
                pattern="^[a-zA-Z\\s]+$",
                examples={
                    "valid_username": {
                        "title": "Корректное имя пользователя",
                        "value": "Urban Uni"
                        },
                    "invalid_username": {
                        "title": "Некорректное имя пользователя",
                        "value": "User123"
                        }
                }
            )
        ],
        age: Annotated[
            int,
            Path(
                ge=18,
                le=120,
                description='Enter age',
                examples={
                    "min_age": {
                        "title": "Минимальный возраст",
                        "value": 18
                    },
                    "max_age": {
                        "title": "Максимальный возраст",
                        "value": 120
                    }
                }
            )
        ]
):
    return {
        "username": username,
        "age": age,
        "message": f"Вы вошли как пользователь {username} возрастом {age} лет"
    }
