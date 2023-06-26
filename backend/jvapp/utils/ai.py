import openai
import logging

logger = logging.getLogger(__name__)


def ask(prompt, model='text-curie-001'):
    print(f'Asking {model} the following prompt:\n{prompt}')
    resp = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=1,
        max_tokens=87,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(resp)
    return resp['choices'][0]['text']
