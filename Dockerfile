FROM python:3
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir feedparser tweepy irc pythorhead praw loguru # loguru required for pythorhead
CMD [ "python", "./main.py" ]
