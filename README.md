# **library**
API сервис для управления книжным каталогом (библиотекой). Проект написан на python 3.9.

Стек: Django, GraphQL, PostgreSQL, docker-compose, poetry

### **Базовые модели проекта**
- **Author**: авторы
- **Genre**: жанры
- **Publisher**: издатели
- **Book**: книги

### **Запуск стека приложений с помощью docker-compose**
Склонируйте репозиторий. 

Выполните команду `docker-compose up -d --build` для запуска сервера.

Выполните миграции: `docker-compose exec app bash -c "cd drf/ && python manage.py migrate"`.

Создайте суперпользователя: 

`docker-compose exec app bash -c "cd drf/ && python manage.py createsuperuser"`

Для просмотра БД доступна админ-панель pgAdmin 
http://localhost:5050/
```
login: admin@admin.com
password: admin
```

Далее подключаемся к БД:
```
Object -> Register -> Server...
name: library_db
```
Во вкладке **Connection**:
```
Host name: db
Port: 5432
Maintenance database: postgres
Username: postgres
Password: postgres
```
Просмотр таблицы по пути:
```
library_db -> Databases -> postgres -> Schemas -> public -> Tables
```

### **Django admin panel**

Доступен список всех моделей, их создание, редактирование и выгрузка выбранного списка объектов по каждой модели в формате CSV.

### **API методы**

API запросы выполняются с помощью GraphQL доступного через интерфейс GraphiQL http://127.0.0.1:8000/graphql

В GraphiQL в документации описаны все доступные запросы (query) и мутации (mutation).

### **Query**

Запросы на получение доступны для всех моделей, также для каждой модели доступна фильтрация, сортировка по всем полям и дополнительные параметры запроса *offset, before, after, first, last*.

Результат запроса включает в себя параметры:
- pageInfo: информация о пагинации
- edges: содежит результат запроса (в поле *node*)
- totalCount: общее количество результатов
- edgeCount: количество результатов на странице

### **Пример запроса**

Создадим фрагменты для каждой модели для удобного получения результатов.

```
fragment AuthorFragment on AuthorType {
  id
  firstName
  middleName
  lastName
  birthDate
}

fragment GenreFragment on GenreType {
  id
  title
}

fragment PublisherFragment on PublisherType {
  id
  title
}

fragment BookFragment on BookType {
  id
  title
  author {
    ...AuthorFragment
  }
  genre {
    edges {
      node {
        ...GenreFragment
      }
    }
  }
  publisher {
    ...PublisherFragment
  }
}
```

Создадим автора, жанр и издателя:

```
mutation createAuthor {
  createAuthor(
    input: {firstName: "Виктор", middleName: "Алексеевич" lastName: "Петров", birthDate: "1980-09-17"}
  ) {
    ok
    author {
      ...AuthorFragment
    }
  }
}

mutation createGenre {
  createGenre(input: {title: "Сказка"}) {
    ok
    genre {
      ...GenreFragment
    }
  }
}

mutation createPublisher {
  createPublisher(input: {title: "Орел"}) {
    ok
    publisher {
      ...PublisherFragment
    }
  }
}
```

Результат:

```
{
  "data": {
    "createAuthor": {
      "ok": true,
      "author": {
        "id": "5",
        "firstName": "Виктор",
        "middleName": "Алексеевич",
        "lastName": "Петров",
        "birthDate": "1980-09-17"
      }
    }
  }
}

{
  "data": {
    "createGenre": {
      "ok": true,
      "genre": {
        "id": "3",
        "title": "Сказка"
      }
    }
  }
}

{
  "data": {
    "createPublisher": {
      "ok": true,
      "publisher": {
        "id": "3",
        "title": "Орел"
      }
    }
  }
}
```

Создадим 2 книги, указав *id* автора, жанра и издателя:


```
mutation createBook {
  createBook(
    input: {title: "Сказки", author: {id: 5}, genre: [{id: 3}], publisher: {id: 3}}
  ) {
    ok
    book {
      ...BookFragment
    }
  }
}

mutation createBook {
  createBook(
    input: {title: "Сказки. Часть 2", author: {id: 5}, genre: [{id: 3}], publisher: {id: 3}}
  ) {
    ok
    book {
      ...BookFragment
    }
  }
}
```
Результат:

```
{
  "data": {
    "createBook": {
      "ok": true,
      "book": {
        "id": "2",
        "title": "Сказки",
        "author": {
          "id": "5",
          "firstName": "Виктор",
          "middleName": "Алексеевич",
          "lastName": "Петров",
          "birthDate": "1980-09-17"
        },
        "genre": {
          "edges": [
            {
              "node": {
                "id": "3",
                "title": "Сказка"
              }
            }
          ]
        },
        "publisher": {
          "id": "3",
          "title": "Орел"
        }
      }
    }
  }
}
```

Мы хотим получить все книги, которые написал наш автор. Запрос будет следующим:

```
query author {
  author(id: 5) {
    totalCount
    edges {
      node {
        books {
          edges {
            node {
              ...BookFragment
            }
          }
        }
      }
    }
  }
}
```

Результат:

```
{
  "data": {
    "author": {
      "totalCount": 1,
      "edges": [
        {
          "node": {
            "books": {
              "edges": [
                {
                  "node": {
                    "id": "3",
                    "title": "Сказки. Часть 2",
                    "author": {
                      "id": "5",
                      "firstName": "Виктор",
                      "middleName": "Алексеевич",
                      "lastName": "Петров",
                      "birthDate": "1980-09-17"
                    },
                    "genre": {
                      "edges": [
                        {
                          "node": {
                            "id": "3",
                            "title": "Сказка"
                          }
                        }
                      ]
                    },
                    "publisher": {
                      "id": "3",
                      "title": "Орел"
                    }
                  }
                },
                {
                  "node": {
                    "id": "2",
                    "title": "Сказки",
                    "author": {
                      "id": "5",
                      "firstName": "Виктор",
                      "middleName": "Алексеевич",
                      "lastName": "Петров",
                      "birthDate": "1980-09-17"
                    },
                    "genre": {
                      "edges": [
                        {
                          "node": {
                            "id": "3",
                            "title": "Сказка"
                          }
                        }
                      ]
                    },
                    "publisher": {
                      "id": "3",
                      "title": "Орел"
                    }
                  }
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```

