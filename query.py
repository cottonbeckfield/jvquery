import os
import logging
import urllib


BOT_TOKEN = os.environ["BOT_TOKEN"]
SLACK_URL = os.environ["POST_URL"]


def lambda_handler(data, context):

    slack_event = data['event']

    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        text = slack_event["text"]
        if text == "hot wash":
            definition = "lessons learned"
        end

        channel_id = slack_event["channel"]

        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("term", text)
                ("definition", definition)
            )
        )
        data = data.encode("ascii")

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
