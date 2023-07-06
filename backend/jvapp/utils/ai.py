import hashlib
import json
import os

import openai
import logging

from jvapp.models.tracking import AIRequest

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPEN_AI_API_KEY')


DEFAULT_MODEL = 'text-davinci-003'


class PromptError(Exception):
    pass

class PromptRequestError(PromptError):
    pass

class PromptParseError(PromptError):
    pass

def ask(prompt, model=DEFAULT_MODEL):
    """Make a request to OpenAI and return a structured result.

    Model descriptions: https://platform.openai.com/docs/models/gpt-3-5

    Returns:
        dict that is a parse of the response text from JSON
        aiRequest object with
    """
    # Check to see if we've made this prompt before
    prompt_hash = hashlib.md5(bytes(prompt + model, 'UTF-8')).hexdigest()
    if existing := AIRequest.objects.filter(prompt_hash=prompt_hash).first():
        if existing.result_status == AIRequest.RESULT_STATUS_SUCCESS:
            resp = json.loads(existing.response)
            return json.loads(resp['choices'][0]['text']), existing
        if existing.result_status == AIRequest.RESULT_STATUS_UNPARSEABLE:
            raise PromptParseError

    request_tracker = AIRequest(
        prompt_hash=prompt_hash,
    )
    try:
        print(f'Asking {model} the following prompt:\n{prompt}')
        resp = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=1,
            max_tokens=2500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        request_tracker.response = json.dumps(resp)
        print(f'Received response: {resp}')
    except Exception as ex:
        request_tracker.result_status = request_tracker.RESULT_STATUS_ERROR
        request_tracker.save()
        raise PromptRequestError from ex

    try:
        data = json.loads(resp['choices'][0]['text'])
    except json.JSONDecodeError as ex:
        request_tracker.result_status = request_tracker.RESULT_STATUS_UNPARSEABLE
        request_tracker.save()
        raise PromptParseError from ex

    request_tracker.result_status = request_tracker.RESULT_STATUS_SUCCESS
    request_tracker.save()
    return data, request_tracker

