def prepare_feedback(text: str, elements: tuple):
    feedback_text = FIRST_TEXT
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

    if elements[1] > elements[2] or elements[1] < MIN_CLAIMS or elements[2] < MIN_PREMISES:
        if elements[1] < MIN_CLAIMS:
            feedback_text += MORE_CLAIMS_TEXT
        else:
            feedback_text += UNSUPPORTED_CLAIMS_TEXT
    else:
        feedback_text += GOOD_ARGUMENT_TEXT
    return feedback_text