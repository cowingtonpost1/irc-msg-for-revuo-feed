from notifier import Notifier
import irc3
from irc3.plugins.command import command
import threading
import time

class IRCNotifier(Notifier):
    def __init__(self, server, port, channels, nickname, password, format, use_sasl=False, sasl_username=None):
        self.server = server
        self.port = port
        self.channels = set(channels)
        self.nickname = nickname
        self.password = password
        self.format = format
        self.use_sasl = use_sasl
        self.sasl_username = sasl_username or nickname
        self.connected = False

        config = {
            'nick': nickname,
            'autojoins': list(channels),
            'host': server,
            'port': port,
            'ssl': port == 6697,
            'includes': ['irc3.plugins.core'],
        }

        if use_sasl:
            config['includes'].append('irc3.plugins.sasl')
            config['sasl_username'] = self.sasl_username
            config['sasl_password'] = self.password
        elif password:
            config['includes'].append('irc3.plugins.autocommand')
            config['autocommands'] = ["PRIVMSG NickServ :IDENTIFY " + password]


        self.bot = irc3.IrcBot.from_config(config)

    def is_ready(self):
        return self.connected

    def run(self):
        self._log(f"Connecting to {self.server}:{self.port} as {self.nickname}...")
        thread = threading.Thread(target=self._run_bot)
        thread.daemon = True
        thread.start()
        time.sleep(1)
        self.connected = True

    def _run_bot(self):
        try:
            self._log("Connected.")
            self.bot.run(forever=True)
        except Exception as e:
            self._log(f"Connection failed: {e}")
            self.connected = False

    def send_message(self, message):
        if not self.connected:
            self._log("Not connected. Cannot send message.")
            return

        for channel in self.channels:
            self.bot.privmsg(channel, message)
            self._log(f"Sent message to {channel}: {message}")

    def _log(self, txt):
        print(f"IRC {self.server}: {txt}")

