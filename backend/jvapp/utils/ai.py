import os

import openai
import logging

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPEN_AI_API_KEY')


def ask(prompt, model='text-davinci-003'):
    # Model descriptions: https://platform.openai.com/docs/models/gpt-3-5
    print(f'Asking {model} the following prompt:\n{prompt}')
    return openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
