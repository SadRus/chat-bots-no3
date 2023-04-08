import os

from google.cloud import dialogflow
from dotenv import load_dotenv


load_dotenv()


def detect_intent_texts(
    text,
    language_code='ru-RU',
):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation.
    """

    session_id = os.getenv('TG_CHAT_ID')
    project_id = os.getenv('PROJECT_ID')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f'Session path: {session}\n')

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

    query_text = response.query_result.query_text
    intent_name = response.query_result.intent.display_name
    intent_confidence = response.query_result.intent_detection_confidence
    fulfillment_text = response.query_result.fulfillment_text

    print(
        '=' * 20 + '\n',
        f'Query text: {query_text}\n',
        f'Detected intent: {intent_name}',
        f'(confidence: {intent_confidence})\n',
        f'Fulfillment text: {fulfillment_text}'
    )
    return fulfillment_text


if __name__ == '__main__':
    detect_intent_texts('vo1cec1tybot', '440084749', 'привет')
