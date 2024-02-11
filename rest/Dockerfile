# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.11-slim-bookworm

ENV FLASK_APP=/app/rest/run.py
ENV FLASK_ENV=development
# Виставляємо робочу директорію контейнера в /app
WORKDIR /app

# Копіюємо файл з залежностями, створюється новий шар
COPY ./rest/requirements.txt requirements.txt

# Встановлюємо залежності вказалі requirements.txt - теж новий шор
RUN pip install --no-cache-dir -r requirements.txt

# Додаємо наш код /app - створили новий шар. таким чином при ребілді не потрібно заново ставити залежності при змані коду
ADD . /app

# Документуємо порт, що використовується контейнером. В компоузі буде юзатися для міжконтейнерного зв'язку
EXPOSE 5000

# Run app.py when the container launches
# https://spacelift.io/blog/docker-entrypoint-vs-cmd
# ENTRYPOINT [ "python" ] 
CMD ["bash", "/app/rest/start_flask.sh"]
