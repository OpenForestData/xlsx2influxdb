FROM python:3.8-slim

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen pl_PL.CP1250

WORKDIR /app
COPY . /app

RUN pip install -r /app/requirements.txt

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
