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