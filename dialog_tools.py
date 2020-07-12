import dialogflow_v2

LANGUAGE_CODE = 'ru-RU'


def get_answer(project_id, session_id, text, platform_prefix):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, f'{platform_prefix}{session_id}')

    text_input = dialogflow_v2.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    if not ('vk' in platform_prefix and response.query_result.intent.is_fallback):
        return response.query_result.fulfillment_text
