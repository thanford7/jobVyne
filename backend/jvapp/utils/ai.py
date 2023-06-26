import openai
import logging

logger = logging.getLogger(__name__)


def ask(prompt, model='text-curie-001'):
    print(f'Asking {model} the following prompt:\n{prompt}')
    resp = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.1,
        max_tokens=30,
    )
    print(resp)
    return resp['choices'][0]['text']
