import json
import os

from google.cloud import dialogflow
from dotenv import load_dotenv

load_dotenv()


def create_intent(
    display_name,
    training_phrases_parts,
    message_texts,
):
    """Create an intent of the given intent type.
    """

    project_id = os.getenv('PROJECT_ID')
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part,
        )

        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    request = {
        "parent": parent,
        "intent": intent,
    }
    response = intents_client.create_intent(request)

    print("Intent created: {}".format(response))


with open('dvmn_intents.json', 'r') as file:
    intents = json.load(file)


for intent_name, phrases in intents.items():
    create_intent(
        display_name=intent_name,
        training_phrases_parts=phrases['questions'],
        message_texts=[phrases['answer']],
    )
