from fastapi import FastAPI, Query

# Создаем экземпляр приложения FastAPI
app = FastAPI()


# Маршрут к главной странице - "/"
@app.get('/')
def home_page():
    return {"message": 'Главная страница'}


# Маршрут к странице администратора - "/user/admin": http://127.0.0.1:8000/user/admin
@app.get("/user/admin")
def get_admin():
    return {"message": "Вы вошли как администратор"}


# Маршрут к страницам пользователей с передачей данных в адресной строке - "/user":
# http://127.0.0.1:8000/user?username=%27Oleg%27&age=58
@app.get('/user')
async def get_user_info(username: str = Query(...), age: int = Query(...)):
    user_info = {"username": username, "age": age}
    return user_info


@app.get("/user")
async def get_user_info_(username: str = Query(...), age: int = Query(...)):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}


# Маршрут к страницам пользователей с параметром в пути - "/user/{user_id}"
# @app.get('/user/{user_id}')
# async def get_user_(user_id: int):
#     return f'Вы вошли как пользователь № {user_id}'


# @app.get("/user/{user_id}")
# async def get_user(user_id: int):
#     return {"message": f"Вы вошли как пользователь № {user_id}"}


# Маршрут к страницам пользователей с параметром в пути - "/user/{user_id}": http://127.0.0.1:8000/user/3

users = {
    1: {"username": "user1", "age": 25},
    2: {"username": "user2", "age": 30},
    3: {"username": "user3", "age": 22},
}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    user = users.get(user_id)
    if user:
        return {"message": f"Информация о пользователе. ID: {user_id}, Имя: {user['username']}, Возраст: {user['age']}"}
    else:
        return {"message": "Пользователь не найден"}
