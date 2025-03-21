from irc_notifier import IRCNotifier

"""Uncomment for twitter notification support"""
# from twitter_notifier import TwitterNotifier

feed_url = "https://revuo-xmr.com/atom.xml"
savefile_path = "/app/save.pickle/save.pickle"
reload_minutes = 1

notifiers = [
    IRCNotifier(
        server="irc.libera.chat",
        port=6667,
        channels=["#cow123-irc-testing"],
        nickname="revuoxmr",
        password=None,
        format="Revuo Monero {title}. {link}",
        use_sasl=False, # set to True to use SASL authentication
        # sasl_username="usernamehere", # Useful if SASL account username is different from nickname, not usually required.
    ),
]

# Twitter notifier example, requires tweepy library.
"""
notifiers.append(TwitterNotifier(
    consumer_key="",
    consumer_secret="",
    access_token="",
    access_token_secret="",
    format="We're pleased to share Revuo #Monero {title} is now available! {link}",
))
"""
