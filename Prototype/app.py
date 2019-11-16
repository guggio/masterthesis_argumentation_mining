import slack
import ssl as ssl_lib
import certifi
from ArgumentBot.argument_bot import ArgumentBot
from farm.infer import Inferencer

argument_bot_sent = {}

SLACK_BOT_TOKEN = "<TOKEN>"


def start_argument_bot(web_client: slack.WebClient, user_id: str, channel: str):
    argument_bot = ArgumentBot(channel)

    welcome = argument_bot.get_message_payload()

    response = web_client.chat_postMessage(**welcome)

    argument_bot.timestamp = response["ts"]

    if channel not in argument_bot_sent:
        argument_bot_sent[channel] = {}
    argument_bot_sent[channel][user_id] = argument_bot


@slack.RTMClient.run_on(event="message")
def message(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    if text and text.lower() == "start":
        return start_argument_bot(web_client, user_id, channel_id)

    if "subtype" not in data:
        argument_bot = ArgumentBot(channel_id)
        elements = predict_components(data.get("text"))
        feedback = prepare_feedback(data.get("text"), elements)
        response = argument_bot.get_feedback_payload(feedback)
        web_client.chat_postMessage(**response)


def load_bert_model():
    """Load in the pre-trained model"""
    global model
    save_dir = 'Model'
    model = Inferencer.load(save_dir)


def predict_components(text: str):
    text_to_analyze = [{'text': '{}'.format(text)}]
    result = model.inference_from_dicts(dicts=text_to_analyze)

    annotated_text = [[i['label'], i['start'], i['end']] for i in result[0]['predictions'] if
                      i['probability'] > 0.75]
    count = 0
    count_claim = 0
    count_premise = 0
    elements = []
    for ann in annotated_text:
        if ann[0] != 'O':
            elements.append({
                'id': count,
                'label': ann[0].lower(),
                'start': ann[1],
                'end': ann[2]
            })
            if ann[0].lower() == 'claim':
                count_claim += 1
            else:
                count_premise += 1
        else:
            continue
        count += 1

    return elements, count_claim, count_premise


def prepare_feedback(text: str, elements: tuple):
    feedback_text = "Hier kommt das Feedback zu Deiner Argumentation, " \
                    "Claims werden *fett* und Premises _kursiv_ dargestellt:\n\n\n"
    before = 0
    for e in elements[0]:
        start = e['start']
        end = e['end']
        marker = '*' if e['label'] == 'claim' else '_'
        feedback_text += text[before:start]
        feedback_text += marker
        feedback_text += text[start:end]
        feedback_text += marker
        before = end
    if before == 0:
        feedback_text += text

    if elements[1] > elements[2] or elements[1] < 2:
        if elements[1] < 2:
            feedback_text += "\n\nIch würde dir empfehlen, deinen Text noch argumentativer zu gestalten. " \
                             "Versuche mindestens zwei Claims mit relevanten Premises zu stützen\n"
        else:
            feedback_text += "\n\nIch würde dir empfehlen, deinen Text noch argumentativer zu gestalten. " \
                             "Versuche Deine Claims besser mit relevanten Premises zu stützen\n"
    else:
        feedback_text += "\n\nIch empfinde Deine Argumentation als gelungen! " \
                         "Du hast mehrere Aussagen gemacht und diese mit relevanten Premises gestützt. Weiter so!\n"
    return feedback_text


if __name__ == "__main__":
    load_bert_model()
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = SLACK_BOT_TOKEN
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
