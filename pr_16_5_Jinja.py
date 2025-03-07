"""
Таблица основных тегов html с примерами:
https://uguide.ru/tablica-osnovnykh-tegov-html-s-primerami
"""

from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Annotated, List


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# old get
@app.get("/users", response_model=List[User])
async def get_users_():
    return users

"""
Напишите новый запрос по маршруту '/':
    Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
    TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и 
    список users. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
"""

# new get
@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}', response_class=HTMLResponse)
async def get_user_id(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user:
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    return {"error": "Пользователь не найден"}

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
async def create_user(user: UserCreate) -> User:  # переменная user, по которой FastAPI создает объект класса UserCreate
    if any(u.username == user.username for u in users):  # или альтернативно: if user.username in [u.username for u in users]:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


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
    if any(u.username == username for u in
           users):  # или альтернативно: if user.username in [u.username for u in users]:
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
        age: Annotated[
            int,
            Path(
                description="Enter age"
            )
        ]
):
    if users:
        for user in users:
            if user.id == user_id:  # в моей модели User пользователь называется id, а не user_id
                user.username = username  # user[username] не правильно, так как не словарь, а объект и
                # 'username' не правильно, тогда жестко задаю именно 'username', а надо передать параметр username
                user.age = age
                return user
        else:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    raise HTTPException(status_code=404, detail="Список пустой")


@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)  # или del users[i] - удаление по индексу
            return {"detail": f"Пользователь {user_id} удален"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


"""
<!DOCTYPE html>     - тип документа, ! - не обычный тег, а декларация типа, <> обозначение тега
<html lang="en">    - открывает документ, язык страницы английский
<head>              - открывает секцию метаданных
    <meta charset="UTF-8">  - кодировка документа
    <title>FastAPI</title>  - заголовок страницы на вкладке, не меняемая
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
          
          ! Мы подключаем Bootstrap CSS (Cascading Style Sheets) через CDN (Content Delivery Network)
            - CSS — это язык стилей, который используется для описания внешнего вида HTML-документов. Он определяет,
            как элементы HTML должны отображаться на странице: цвет, шрифты, отступы, размеры, расположение ...
            - CDN — это распределенная сеть серверов, которая доставляет контент (пример, CSS, JavaScript, изображения) 
            пользователям с высокой скоростью. Серверы CDN расположены в разных географических точках, что позволяет 
            доставлять контент быстрее, так как он загружается с ближайшего к пользователю сервера
          - Тег <link> используется для подключения внешних ресурсов к HTML-документу. В данном случае он подключает 
          внешнюю таблицу стилей (CSS)
          - Атрибут href (Hypertext Reference) указывает путь к ресурсу, который нужно подключить
          В данном случае это URL-адрес CSS-файла Bootstrap 5, размещенного на CDN (Content Delivery Network) — сервисе, 
          который обеспечивает быструю доставку файлов пользователям. Путь указывает на мини версию CSS-файла 
          (bootstrap.min.css), что уменьшает его размер и ускоряет загрузку
          - rel="stylesheet", атрибут rel (Relationship) определяет связь между документом и подключаемым ресурсом. 
          Значение stylesheet указывает, что подключаемый файл является таблицей стилей (CSS), которая будет 
          использоваться для оформления HTML-документа
          - integrity= атрибут integrity обеспечивает проверку целостности подключаемого файла. Он содержит хэш 
          (в данном случае SHA-384), который браузер использует для проверки, что содержимое файла ок после загрузки.
          Если хэш файла не совпадает с указанным значением, браузер не будет использовать этот файл, что защищает
          от потенциальных атак, связанных с подменой ресурсов
          crossorigin= атрибут crossorigin определяет, как браузер должен обрабатывать запросы к ресурсам с других 
          доменов (Cross-Origin Resource Sharing, CORS). Значение anonymous означает, что запрос к ресурсу (в данном 
          случае CSS-файлу) будет отправлен без учетных данных (например, cookies или HTTP-аутентификации). Это важно
          для безопасности, чтобы предотвратить утечку данных пользователя при загрузке внешних ресурсов
          - Что делает Bootstrap CSS?
          Bootstrap — это популярный CSS-фреймворк, который предоставляет готовые стили и компоненты для быстрой 
          разработки современных и адаптивных веб-интерфейсов. Его CSS-файл содержит:
            Глобальные стили (например, сброс стилей по умолчанию для браузеров).
            Классы для сетки (Grid System), которые позволяют создавать адаптивные макеты.
            Готовые компоненты (кнопки, формы, навигационные панели, карточки и т.д.).
            Утилиты (классы для отступов, цветов, выравнивания и других часто используемых свойств).
            Использование Bootstrap значительно ускоряет разработку, так как вам не нужно писать CSS с нуля.
            
    https: — Схема (протокол).
        Указывает, какой протокол используется для доступа к ресурсу. В данном случае это HTTPS (HyperText Transfer 
        Protocol Secure), который обеспечивает безопасное соединение между браузером и сервером.
    //cdn.jsdelivr.net — Домен (хост).
        Это адрес сервера, на котором находится ресурс. Здесь это CDN (Content Delivery Network) — cdn.jsdelivr.net.
        Домен указывает, куда браузер должен отправить запрос.
    /npm/bootstrap@5.3.2/dist/css/bootstrap.min.css — Путь (маршрут).
        Это путь к конкретному ресурсу на сервере. Давайте разберем его по частям:
            /npm/ — указывает, что ресурс находится в разделе npm (Node Package Manager) на CDN.
            bootstrap@5.3.2 — указывает версию Bootstrap (в данном случае 5.3.2).
            /dist/css/ — путь к папке, где находятся CSS-файлы.
            bootstrap.min.css — имя файла. Суффикс .min означает, что файл минифицирован 
            (удалены пробелы, комментарии и т.д. для уменьшения размера).
            
</head> - тег, закрывающий секцию метаданных
<body>  - тег, открывающий видимую часть содержимого страницы
<header>    - тег, открывающий секцию хедера: с навигацией, логотипом, заглавием...
    <nav class="navbar">    - навигационная панель открыта
        <div class="p-3 mb-2 bg-primary text-white">- Контейнер с классами Bootstrap:
                                                            p-3 — внутренние отступы (padding).
                                                            mb-2 — отступ снизу (margin-bottom).
                                                            bg-primary — синий фон (цвет Bootstrap).
                                                            text-white — белый текст.
                                                    - <div> (от англ. division — раздел) — это блочный элемент, 
                                                    который используется для группировки других элементов и создания 
                                                    структуры на веб-странице. Сам по себе <div> не имеет семантического 
                                                    значения (в отличие от тегов <header>, <main>, <section> и т.д.), 
                                                    но он полезен для стилизации и организации контента.
            <h1>CRUD Application</h1>   - Заголовок первого уровня, который отображает название приложения
        </div>
    </nav>                  - навигационная панель закрыта
</header>                   - секция хедера закрыта
<div class="container-fluid"> - Контейнер для содержимого страницы. Этот класс делает контейнер на всю ширину страницы
    {% block container %}  - Это шаблонный тег (используется в шаблонизаторах, как Jinja2). Он определяет блок, 
                                который может быть переопределен в дочерних шаблонах. В этом месте будет вставлено 
                                содержимое, специфичное для конкретной страницы

    {% endblock %}
</div>      - 
</body> - видимая част закрыта
</html> - закрывает структуру документа

{% extends 'main.html'%}
{% block container %}
    {% if user %}
        <article class="card container fluid"></article>
        <br>    - Тег <br> (от англ. break — разрыв) используется для вставки переноса строки в тексте.
                - Он создает разрыв строки, и текст после него начинается с новой строки.
        <!-- Напишите свой код здесь (Вывод свойств объекта User) -->
                - Конструкция <!-- ... --> используется для добавления комментариев в HTML-код.
                - Комментарии не отображаются на странице, но видны в исходном коде. Они полезны для пояснения кода или 
                временного отключения части кода
    {% else %}
            <section class="container-fluid">
                <h2 align="center"> Users </h2>
                <br>
                <div class="card">
                    <ul class="list-group list-group-flush">
                        <!-- Напишите свой код здесь (перебор пользователей) -->
                    </ul>
                </div>
            </section>
    {% endif %}
{% endblock %}
"""