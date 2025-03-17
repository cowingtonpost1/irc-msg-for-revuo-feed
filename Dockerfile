FROM python:3
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir feedparser tweepy irc
CMD [ "python", "./main.py" ]
