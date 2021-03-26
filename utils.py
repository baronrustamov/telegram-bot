'''
import os
#from gnewsclient import gnewsclient
#from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID, DIALOGFLOW_KEY, WIT_TOKEN, LANG
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "newsbotclient.json"
#dialogflow_session_client = dialogflow.SessionsClient()

clientn = gnewsclient.NewsClient()

'''
def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(config.PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result
'''
def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
    clientn.language = 'language'
    #clientn.location = parameters.get('geo-country')
    clientn.topic = 'topic'
    return clientn.get_news()[:5]


topics_keyboard = [
    ['Top Stories', 'World', 'Nation'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science', 'Health']
]

'''