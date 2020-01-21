import os
import logging
import urllib.request

# Phrases TO-DO
#  Juice worth the squeeze
# - Baby powder their feet
# - At the end of the day
# - Getting pregnant with other teams
# - The sugar that helps make the medicine go down
# - Taking away someone's birthday
# - Making sure we're not destroying christmas
# - Half pregnant
# - They're a great American
# - "Seems nice enough but I’m not exactly sure there is much going on between the ears "
# - Press
# - Dingus
# - Let's rap about it on x day
# - I drank his milkshake yesterday and he's probably a bit sore.
# - mother fucking plato looking mother fucker
# - Dropping the kids off at the pool
# - Even I lose a marble or two once in a while.

# Environmental Variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
SLACK_URL = os.environ["SLACK_URL"]


def lambda_handler(data, context):

    print(data['event'])
    if "challenge" in data:
        return data["challenge"]

    # Dictionary of Visneski-isms
    jvdict = {
        "hot wash":"lessons learned",
        "press": "move forward"
    }

    # Handling some potential errors
    slack_event = data['event']
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
        return

    text = slack_event["text"]
    if not text in jvdict:
        logging.warn("Unknown phrase")
        return

    # Setting up the definition, and searching the dict for the
    # relevant word search.
    definition = jvdict[text]
    channel_id = slack_event["channel"]

    # Format data and request values.
    data = urllib.parse.urlencode(
        (
            ("token", BOT_TOKEN),
            ("channel", channel_id),
            ("term", text),
            ("definition", definition)
        )
    )
    data = data.encode("ascii")

    print(data)

    # Send definition back to Slack.
    request = urllib.request.Request(
        SLACK_URL,
        data=data,
        method="POST"
    )

    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

    urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"
