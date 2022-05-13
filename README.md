# Порядок запуска проекта
## Настройка локального окружения
Только для PyCharm Pro
...
## Локальный запуск проекта
Открыть окно терминала и запустить
```bash
docker-compose up --build
```
В браузере открыть [http://localhost:8000/admin](http://localhost:8000/admin). В окне терминала можно видеть http-запросы проекта.
# Деплой
Пример команды копирования файлов на удаленный сервер
```commandline
scp -i ~\.ssh\yandex-cloud -r budget sergey@51.250.48.190:/home/sergey/django_budget
```