from google.cloud import dialogflow


def detect_intent_texts(text, session_id, project_id, language_code='ru-RU'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation.
    """

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text,
        language_code=language_code
    )
    query_input = dialogflow.QueryInput(text=text_input)

    request = {
        'session': session,
        'query_input': query_input
    }
    response = session_client.detect_intent(request)

    intent_content = {
        'query_text': response.query_result.query_text,
        'intent_name': response.query_result.intent.display_name,
        'intent_confidence': response.query_result.intent_detection_confidence,
        'fulfillment_text': response.query_result.fulfillment_text,
        'is_fallback': response.query_result.intent.is_fallback,
    }
    return intent_content
