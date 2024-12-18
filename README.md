# Проектная работа: диплом

Команда: [Артём](https://github.com/Benrise)

Тема: Ассистент

Задача: Сделайте интеграцию между вашим сервисом поиска фильмов и голосовым помощником. Сценарий следующий: вы говорите помощнику, что найти, он делает запрос в ваш сервис для ES, получает ответ и зачитывает его. Если вариантов несколько, то зачитывается первый вариант. 

### Поток данных

Пользовательский запрос (голосовой ввод) → Speech Service (получение транскрипции) → Intent Classifier Service (классификация намерения) → Translate Transcript (перевод транскрипции) -> Extract Entity (извлечение сущностей) -> Search Service (обращение к сервису контента).

### Роли моделей

1. Intent Classifier - классифицирует намерения пользователя по заранее заданным меткам. Далее эти метки определяют тип запроса к сервису поиска.
2. Translate Transcript - перевод транскрипции. Необходим для поиска фильмов и жанров, т.к. в базе данных они записаны на английском языке.
3. Extract Entity - извлекает сущности, если такие имеются (персоны, фильм, жанр).

**Таким образом:**

Система способна реагировать согласно тем данным, которые есть в Elasticsearch.

### Примеры

**Намерение:** пользователь хочет получить авторов фильма
![image](https://github.com/user-attachments/assets/0c9d4e52-e959-40be-80b6-f0aebe62675a)


**Намерение:** пользователь хочет узнать продолжительность фильма
![image](https://github.com/user-attachments/assets/78504771-07f5-4bcd-b904-5335892c191c)

### Jupyter ноутбук

Файл model.ipynb подробно описывает процесс разработки ML части проекта:

1. Формирование зависимостей и технологий
2. Примеры данных, которые хранятся в ES и служат ориентиром для получения сущностей (заголовки жанров и фильмов)
3. Формирование датасета для распознования намерения
4. Реализация перевода на основе модели 'Helsinki-NLP/opus-mt-ru-en'
5. Реализация Classify User Intention с использованием логистической регрессии и векторизатора, выгрузка моделей
6. Реализация Entity Extracting, получения сущностей из транскрипции (людей, фильмов и жанров)

**Датасет для обучения Classify User Intention**

Для обучения модели был сформирован типовой датасет по соответствующим меткам.
Подобный подход позволяет легко добавлять новые типы запросов, масштабировать систему, а также обрабатывать синонимы и различные варианты фраз.
```
intent_dataset = {
    "get_film_duration": [
        ...,
        "Сколько идет фильм",
        "Длительность фильма",
        "Продолжительность фильма",
        ...,
    ],
    "get_film_genre": [
        ...,
        "Какой жанр у фильма",
        "Что за жанр у фильма",
        "Жанр фильма",
        ...,
    ],
    "get_film_rating": [
        ...,
        "Рейтинг",
        "Рейтинг фильма",
        "Какой рейтинг у фильма",
        ...,
    ],
    ...
```

### Основная бизнес логика сервиса
При запуске экземпляра сервиса происходит инициализация Redis, Scheduler и LifespanManager.

**Redis**
- cлужит для кэширования получения списков заголовков фильмов и жанров с сервиса контента. С ними работает Entity Extracting. Помимо этого, Redis также кэширует все запросы, исходящие от внутреннего сервиса поиска

**Scheduler**
- в заданный интервал времени получает список заголовков фильмов и жанров у сервиса контента с принудительным обновлением кэша. Таким образом достигается актуализация данных.

**LifespanManager**
- реализует функцию обновления данных о заголовках фильмов жанров, а также содержит метод загрузки NER модели для Entity Extracting

API сервиса представляет собой одну единственную ручку `/assistant/api/v1/search`. 
- **принимает:** аудиофайл
- **возвращает:** словарь с данными/аудиофайл для воспроизведения ответа

Пример ответа:
```
{
  "response": "Сценарист(ы) фильма 'Star': Guy Ritchie, Joe Sweet.",
  "transcript": "Авторы фильма звёздные войны",
  "transcript_en": "The film's authors are Star Wars.",
  "intent": "get_film_writers",
  "persons": [],
  "genres": [],
  "films": [
    "Star",
    "Star Wars"
  ]
}
```

**Формиривание запроса**

Формирование запроса происходит по маппингу намерения - intent. В директории mappers есть "мапа", которая по ключу возвращает сформированный запрос в сервис поиска, а также заготовленный ответ.

Пример записей маппинга:
```
{
    Intents.GET_FILM_GENRE.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Жанр фильма '{result['hits']['hits'][0]['_source']['title']}': {', '.join([genre['name'] for genre in result['hits']['hits'][0]['_source'].get('genres', [])])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, жанр фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_RATING.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Рейтинг фильма '{result['hits']['hits'][0]['_source']['title']}' составляет {result['hits']['hits'][0]['_source'].get('imdb_rating', 'неизвестно')}."
            if result.get('hits', {}).get('hits') else f"К сожалению, рейтинг фильма '{films[0]}' найти не удалось."
        ),
    },
    ...
}
```

Отправка запроса и получения данных согласно маппингу где `intent` - определенное моделью намерение пользователя
```
    if intent in INTENT_TO_ACTION_MAPPING:
        action = INTENT_TO_ACTION_MAPPING[intent]
        search_result = await action["method"](search_service, films)
        response_message = action["response"](search_result, films)
    else:
        raise Exception("Намерение не поддерживается.")
```

### Итого
1. Реализован сервис умного голосового помощника, который взаимодействует с пользователем и возвращает результаты полученные с сервиса контента
2. Логика обработки запроса задействует NLP и базовый Machine Learning на основе логистической регрессии
3. Технологии backend: FastAPI, Redis, Httpx
