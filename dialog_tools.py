import dialogflow_v2

LANGUAGE_CODE = 'ru-RU'


def get_answer(project_id, text, tg_session_id=None, vk_session_id=None):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, tg_session_id or vk_session_id)

    text_input = dialogflow_v2.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    if not (vk_session_id and response.query_result.intent.is_fallback):
        return response.query_result.fulfillment_text
