import config
import time
import feedparser
import os
import pickle
import time
import signal

def shutdown(_signum, _frame): 
    print("main: Shutting down notifiers")
    for notifier in config.notifiers:
        if hasattr(notifier, "disconnect") and callable(notifier.disconnect):
            notifier.disconnect()

    exit(0)

def main():
    for notifier in config.notifiers:
        if hasattr(notifier, "run") and callable(notifier.run):
            notifier.run()
    
    attempts = 0 
    while True:
        if attempts > 5:
            print("main: Notifiers could not start, exiting...")
            exit(1)

        ready = True
        for notifier in config.notifiers:
            if not notifier.is_ready():
                ready = False

        if ready:
            print("main: All notifiers ready, starting program...")
            break
        else:
            print("main: Not connected yet, waiting...")
            attempts += 1

        time.sleep(15)
    # wait for IRC to join channels
    time.sleep(15)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    while True: 
        last_msg = None
        if os.path.isfile(config.savefile_path):
            with open(config.savefile_path, 'rb') as handle:
                unserialized_data = pickle.load(handle)
            last_msg = unserialized_data["msg"]
        else:
            last_msg = "~"

        entry = None
        try: 
            feed = feedparser.parse(config.feed_url)
            if not feed.entries or len(feed.entries) == 0:
                print("main: Error occurred downloading feed or no entries in feed, retrying later...")
                time.sleep(config.reload_minutes * 60)
                continue
            entry = feed.entries[0]
        except Exception as e: 
            print("main: Error occurred downloading feed, retrying later...")
            time.sleep(config.reload_minutes * 60)
            continue
        
        # used for backwards compatibility with data file
        msg = f"Revuo Monero {entry['title']}. {entry['link']}"

        if last_msg != msg:
            data = {"msg": msg}
            with open(config.savefile_path, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

            for notifier in config.notifiers:
                notifier.send_message(notifier.format_message(entry['title'], entry['link']))

        time.sleep(config.reload_minutes * 60)

if __name__ == "__main__":
    main()
