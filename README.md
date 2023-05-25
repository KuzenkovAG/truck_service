# Truck Service API
API сервис для отслеживания грузов

## Особенности
- Создание грузов (вес груза от 1 до 1000кг);
- Поиск ближайших машин до груза (<= 450 миль);
- Отслеживание текущего местонахождения машин;
- Более 30 000 локаций;
- Расстояние указывается в милях.

## Tech
- Python 3.9
- Django 4.2.1

## Установка (Windows)
Клонируйте репозиторий
```sh
git clone https://github.com/KuzenkovAG/truck_service.git
```
Перейдите в каталог
```sh
cd truck_service/
```
Запуск в контейнере Docker
```sh
docker-compose up
```


## Использование
Создание груза
```sh
POST: http://127.0.0.1:8000/api/v1/loads/
```
```sh
{
    "pick_up": "00617",
    "delivery": "00602",
    "weight": integer,
    "description": "text" 
}
```

Получение информации о грузах (near_trucks - ближайшие до груза машины <= 450 миль)
```sh
GET: http://127.0.0.1:8000/api/v1/loads/
```
```sh
[
    {
        "id": 1,
        "pick_up": "00617",
        "delivery": "00617",
        "near_trucks": 1
    }
]
```
Получение информации о грузе
```sh
GET: http://127.0.0.1:8000/api/v1/loads/{id}/
```
```sh
{
    "id": 1,
    "pick_up": "00617",
    "delivery": "00617",
    "weight": integer,
    "description": "text",
    "trucks": [
        {
            "id": integer,
            "truck": "1199V",
            "distance": integer
        },
        {
            "id": integer,
            "truck": "1198A",
            "distance": integer
        }
    ]
}
```
Редактирование груза
```sh
PUT/PATCH: http://127.0.0.1:8000/api/v1/loads/{id}/
```
```sh
Payload:
{
    "weight": integer,
    "description": "text",
}
Response sample:
{
    "id": integer,
    "pick_up": "00617",
    "delivery": "00602",
    "weight": integer,
    "description": "text"
}
```
Удаление груза
```sh
DELETE: http://127.0.0.1:8000/api/v1/loads/{id}/
```

Редактирование локации машины
```sh
PUT/PATCH: http://127.0.0.1:8000/api/v1/trucks/{id}/
```
```sh
Payload:
{
    "location": "00602",
}
Response sample:
{
    "id": integer,
    "uid": "1000A",
    "location": "00606",
    "capacity": integer
}
```

## Автор
[Alexey Kuzenkov]


   [Alexey Kuzenkov]: <https://github.com/KuzenkovAG>
