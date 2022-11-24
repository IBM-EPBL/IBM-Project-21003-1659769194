# syntax=docker/dockerfile:1
FROM node:12-alpine
RUN apk add --no-cache python3 pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
