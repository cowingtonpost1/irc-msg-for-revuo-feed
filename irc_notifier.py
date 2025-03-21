from notifier import Notifier
from irc import client
import threading
import time

class IRCNotifier(Notifier):
    def __init__(self, server, port, channels, nickname, password, format, use_sasl=False, sasl_username=None):
        self.server = server
        self.port = port
        self.channels = set(channels)  # Use a set to prevent duplicates
        self.nickname = nickname
        self.password = password
        self.reactor = client.Reactor()
        self.connection = None
        self.thread = None
        self.format = format
        self.connected = False
        self.use_sasl = use_sasl
        self.sasl_username = sasl_username or nickname
        self.rejoin_counter = 0
        self.shutdown = False

    def is_ready(self):
        return self.connected

    def connect(self):
        self._log(f"Connecting to {self.server}:{self.port} as {self.nickname}...")
        try:
            if self.use_sasl: 
                self.connection = self.reactor.server().connect(self.server, self.port, self.nickname, password=self.password, sasl_login=self.sasl_username)
            else: 
                self.connection = self.reactor.server().connect(self.server, self.port, self.nickname)
            self.reactor.add_global_handler("welcome", self.on_connect)
            self.reactor.add_global_handler("disconnect", self.on_disconnect)
        except Exception as e:
            self.connected = False
            self._log(f"Connection error: {e}")
            time.sleep(10)
            self.connect()

    def _log(self, txt): 
        print(f"IRC {self.server}: {txt}")

    def on_connect(self, connection, event):
        self.connected = True
        self._log("Connected to server")
        if self.password and not self.use_sasl:
            self._log("Identifying with NickServ...")
            connection.privmsg("NickServ", f"IDENTIFY {self.password}")
        
        for channel in self.channels:
            self._log(f"Joining {channel}...")
            connection.join(channel)

    def on_disconnect(self, connection, event):
        self.connected = False

        if self.shutdown:
            self._log("Disconnected and program shutting down, not reconnecting...")
            return

        if self.rejoin_counter > 3:
            self._log("Stopping user to prevent join spamming, restart program to try again")
            self.send_message = lambda x, y: self._log("Cannot send message as bot has been disabled due to repeated disconnects") # prevents send_message from crashing program
            while True:
                time.sleep(60)
            
        self._log("Disconnected! Restarting connection in 10 seconds...")
        time.sleep(10)
        self.rejoin_counter += 1
        self.connect()

    def send_message(self, message):
        if self.connection:
            for channel in self.channels:
                try:
                    self._log(f"Sending message to {channel}: {message}")
                    self.connection.privmsg(channel, message)
                except Exception as e:
                    self._log(f"Error sending message to {channel}: {e}")

    def run(self):
        if self.thread and self.thread.is_alive():
            self._log("Thread already running, skipping restart.")
            return

        self.thread = threading.Thread(target=self._run_reactor, daemon=True)
        self.thread.start()

    def _run_reactor(self):
        self.reactor = client.Reactor()
        self.connect()
        while not self.shutdown: 
            self.reactor.process_once(1)

    def disconnect(self):
        self._log("Disconnecting...")
        self.shutdown = True

        if self.connection:
            self.connection.disconnect("Disconnecting from IRC")

        if self.thread:
            self.thread.join()
        
        self._log("Disconnect complete.")


