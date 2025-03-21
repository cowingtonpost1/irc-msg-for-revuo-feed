# irc-msg-for-revuo-feed

```sh
cd /usr/local/src # or wherever
sudo git clone https://github.com/rottenwheel/irc-msg-for-revuo-feed.git
cd irc-msg-for-revuo-feed
docker compose pull
docker compose build
```

## Configuration

Put your configuration variables in `config.py`, which won't be committed to VCS. 

```sh
sudo cp config.example.py config.py
sudo vim config.py
```

## Running

```sh
docker compose up -d
docker compose logs -f # For logging
```

## Nostr Configuration

Run the container interactively and answer the prompts to configure it.

```sh
docker run -v ./nostr-config:/config/ -it ghcr.io/cowingtonpost1/go-nostrss:latest
```

