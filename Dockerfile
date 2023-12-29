FROM python:latest
WORKDIR /root
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip python3-poetry sqlite3 -y

COPY . /root
EXPOSE 8000
RUN poetry install
CMD ["poetry","run","uvicorn","foolish_admin:app","--host","0.0.0.0","--port","8000"]
