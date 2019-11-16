class ArgumentBot:
    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Hallo Argumentation Learner! :wave: Ich freue mich, dass du hier bist. :blush:\n\n"
                "Gerne helfe ich Dir dabei, deine Argumentationsfähigkeiten zu verbessern. "
                "Schreibe doch bitte einen Text, den ich analysieren soll\n\n"
            ),
        },
    }

    def __init__(self, channel):
        self.channel = channel
        self.username = "Argument Bot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
            ],
        }

    def get_feedback_payload(self, text: str):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    },
                }
            ]
        }
