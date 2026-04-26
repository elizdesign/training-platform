from python:3.12

#рабочая папка внутри контейнера
workdir /app

#run - выполн команды внутри контейнера при сборке
#сис пакеты для пайтон библиотек
run apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists*

#коп файлов с комп внутрь контейнера
#сначала завсимости
#ВРЕМЕННО ЗАКОМЕТИРОВАНО(ЖДЕМ ОТ БЭКА)
#copy requirements.txt .
#run pip install --no-cache-dir -r requirements.txt

#коп весь остальной код
copy . . 

#создаем не root-пользователя 
run useradd -m -u 1000 appuser && chown -R appuser:appuser /app
user appuser

#команда, запускающайся при запуске контейнера
cmd ["python", "-c", "print('Docker is ready! Waiting for backend code...')"]




