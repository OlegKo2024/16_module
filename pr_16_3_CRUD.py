from typing import Annotated
from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


# get запрос по маршруту '/users', который возвращает словарь users

@app.get('/users')
async def get_users():
    return users


# написать post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по макс значению ключей
# значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered"

@app.post('/users/{username}/{age}')
async def post_user(username: str, age: int):
    user_id = str(max(int(key) for key in users.keys()) + 1) if users else '1'
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id}, {username} is registered'

# Вариант, если надо добавить несколько записей
#     users.update({user_id: f'Имя: {username}, возраст: {age}'})

# Вариант, если хотим более понятно сделать перебор и проверку условия
#     if users:
#         user_id = str(max(int(key) for key in users.keys()) + 1)
#     else:
#         user_id = '1'

# put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под ключом
# user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"

@app.put('/users/{user_id}')
async def update_user(user_id: str, username: str, age: int):
    if user_id in users.keys():
        users[user_id] = f'Имя: {username}, возраст: {age}'
        return f"The user {user_id} with {username} & {age} is updated"
    else:
        raise HTTPException(status_code=404, detail=f'user: {user_id}, {username} не найдена')



# delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару

@app.delete('/users/{user_id}')
async def delete_user(user_id: str):
    if user_id in users:
        del_user = users[user_id]
        del users[user_id]
        return {"detail": f"User_id: {user_id} {del_user} удален"}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} не найден")

# @app.delete('/users/{user_id}')
# async def delete_user(user_id: str):
#     if users.get(user_id):   # !работает только со списками словарей и показывает и проверяет значение ключа, не ключ!
#         del users[user_id]
#         return {"detail": f"User {user_id} удален"}
#     else:
#         raise HTTPException(status_code=404, detail=f"User {user_id} не найден")
