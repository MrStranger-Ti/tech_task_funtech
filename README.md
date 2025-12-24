# Техническое задание от Funtech

## Установка и запуск

1. Установите [Docker](https://www.docker.com/)
2. Создайте файл `.env` в корне проекта и укажите все обязательные настройки, следуя шаблону в [.env.template](.env.template)
3. Выполните команду для запуска:
   
   ```shell
   docker compose up -d --build
   ```
   
   После этого можно зайти в [SwaggerUI](http://127.0.0.1:8000/docs)

   Для остановки:

   ```shell
   docker compose down
   ```