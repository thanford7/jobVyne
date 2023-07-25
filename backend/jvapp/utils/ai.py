import datetime
import hashlib
import json
import math
import os
import time

import json5
import openai
import logging

from asgiref.sync import sync_to_async

from jvapp.models.tracking import AIRequest

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPEN_AI_API_KEY')

DEFAULT_MODEL = 'gpt-3.5-turbo'


class PromptError(Exception):
    pass


class PromptRequestError(PromptError):
    pass


class PromptParseError(PromptError):
    pass


async def parse_response(openai_response, request_tracker=None):
    if request_tracker:
        request_tracker.response = json.dumps(openai_response)
    content = openai_response['choices'][0]['message']['content']
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # The OpenAI response sometimes includes a trailing comma which causes JSON decoding to fail
        # JSON5 handles trailing commas, but is much slower so we only use it if needed
        try:
            data = json5.loads(content)
        except (json.decoder.JSONDecodeError, ValueError) as ex:
            if request_tracker:
                request_tracker.result_status = request_tracker.RESULT_STATUS_UNPARSEABLE
                await sync_to_async(request_tracker.save)()
            logger.info('Error occurred when parsing model response')
            raise PromptParseError from ex
    
    if request_tracker:
        request_tracker.result_status = request_tracker.RESULT_STATUS_SUCCESS
        await sync_to_async(request_tracker.save)()
    logger.info('Model response successfully parsed')
    return data

WAIT_MULTIPLE_SECONDS = 5


async def send_request(model, prompt, retries=2):
    """ OpenAI has frequent service interruptions so we use exponential backoff
    """
    try_count = 0
    e = openai.error.APIError
    while try_count <= retries:
        try:
            resp = await openai.ChatCompletion.acreate(
                model=model,
                messages=prompt,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return resp
        except (openai.error.ServiceUnavailableError, openai.error.APIError) as e:
            try_count += 1
            wait_seconds = WAIT_MULTIPLE_SECONDS * try_count
            logger.warning(f'Experienced service error with OpenAI. Retrying request in {wait_seconds} seconds.')
            time.sleep(wait_seconds)
    raise e


async def ask(prompt, model=DEFAULT_MODEL, is_test=False):
    """Make a request to OpenAI and return a structured result.

    Model descriptions: https://platform.openai.com/docs/models/gpt-3-5

    Returns:
        dict that is a parse of the response text from JSON
        aiRequest object with
    """
    # Check to see if we've made this prompt before
    prompt_hash = hashlib.md5(bytes(json.dumps(prompt) + model, 'UTF-8')).hexdigest()
    if existing := await sync_to_async(AIRequest.objects.filter(prompt_hash=prompt_hash).first)():
        if existing.result_status == AIRequest.RESULT_STATUS_SUCCESS:
            resp = await parse_response(json.loads(existing.response))
            return resp, existing
        if existing.result_status == AIRequest.RESULT_STATUS_UNPARSEABLE:
            logger.info(f'Previous run of same prompt was un-parseable')
            raise PromptParseError
    
    start_time = datetime.datetime.now()
    logger.info(f'Sending request to {model} model')
    resp = await send_request(model, prompt)
    end_time = datetime.datetime.now()
    model_request_duration = math.ceil((end_time - start_time).total_seconds())
    if is_test:
        print(f'Received response: {resp}')
    else:
        logger.info(f'Received response from {model} model')
        logger.info(f'Duration seconds: {model_request_duration}')

    request_tracker = AIRequest(
        prompt_hash=prompt_hash,
    )
    data = await parse_response(resp, request_tracker=request_tracker)
    return data, request_tracker
