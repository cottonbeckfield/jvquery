# This is a script that expects a user to provide a phrase that JV says
# and returns the human readable meaning back.
# Creator: Cotton Beckfield, 1-31-2020
import os
import logging
import json
import urllib.request

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
        "press": "move forward",
        "They're a great American": "they are an idiot"
    }

    # Handling some potential errors
    slack_event = data['event']
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
        return

    text = slack_event["text"]

    # Setting up the definition, and searching the dict for the
    # relevant word search.
    duplicate_words = ["at", "the", "their", "it", "on", "of", "a", "and", "that",
    "i", "in", "i'm", "not", "go", "we're", "they're", "but", "there"]

    # definition = [val for key, val in jvdict.items() if text in key]
    definition = None
    query_terms = text.split(" ")
    for single_term in query_terms:
        term_to_check = single_term.lower()
        if term_to_check in duplicate_words:
            continue
        for jv_key, jv_value in jvdict.items():
            if term_to_check in jv_key.lower():
                definition = jv_value

    if not definition:
        logging.warning("Unknown phrase")
        return

    print("The definition is:", definition)

    # definition = jvdict[text]
    channel_id = slack_event["channel"]

    print("Sending message to Slack: {}".format(definition))
    json_txt = json.dumps({
        "channel": channel_id,
        "text": definition
    }).encode('utf8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(BOT_TOKEN)
    }

    req = urllib.request.Request(
        SLACK_URL,
        data=json_txt,
        headers=headers
    )
    urllib.request.urlopen(req)

    return "200 OK"
