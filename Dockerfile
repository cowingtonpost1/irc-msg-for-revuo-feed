FROM python:3
WORKDIR /app
RUN pip install --no-cache-dir feedparser tweepy irc3 pythorhead praw loguru # loguru required for pythorhead
COPY . .
CMD [ "python", "./main.py" ]
