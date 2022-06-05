#FROM my_python_base_image
#
#ADD my_app.py .
#
#CMD ["python3", "my_app.py"]

#команды прочие
#docker run -it --name millennium_falcon --mount type=bind,source=C:\Users\Пользователь\PycharmProjects\2.2.YAND_SPRINT_2_NEW_MODELS\movies\host_volume,target=/container_volume ubuntu:18.04 cat container_volume/file.txt

#FROM ubuntu:18.04 RUN echo Easy. Jedi business >> /internal_volume/file.txt VOLUME /internal_volume



#"""новый докер Не работает через такие команды:
#запуск сервера docker build -t simple_server . - эта команда отрабатывает
#запуск докера  который ниже docker run --rm --name srv_1 simple_server
# Вот такая ошибка : docker: Error response from daemon: OCI runtime create failed: container_linux.go:380: starting
#container process caused: exec: "python3": executable file not found in $PATH: unknown.

FROM python:3.9.0-alpine3.12

RUN apk --no-cache add curl
CMD ["python3", "-m", "http.server", "8000"]