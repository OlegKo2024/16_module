from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get('/user/{user_id}')
async def get_user(user_id: Annotated[int, Path(ge=1,
                                                le=100,
                                                description='Enter User ID',
                                                example=1)]
                   ):
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user/{username}/{age}')
async def get_user(username: Annotated[str, Path(min_length=5,
                                                 max_length=20,
                                                 description='Enter username (длина от 5 до 20 символов, только '
                                                             'буквы и пробелы)',
                                                 regex="^[a-zA-Z\\s]+$",
                                                 example="Urban Uni"
                                                 )],
                   age: Annotated[int, Path(ge=18,
                                            le=120,
                                            description='Enter age',
                                            example=25
                                            )]
                   ):
    return {
        "username": username,
        "age": age,
        "message": f"Вы вошли как пользователь {username} возрастом {age} лет"
    }
