import os
import openai 
import logging
from dotenv import load_dotenv
from create_profile_description.schemas import InputSchema


load_dotenv()

def get_logger(__name__):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger(__name__)


SYSTEM_PROMPT = """You are expert at creating a profile description for a user. 
You could include emojis appropriately, but avoid using too many of them.
"""

USER_PROMPT = """Create a profile description for a user given the following points:
Points: {points}
"""
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.3
DEAULT_FILENAME = "output.txt"


def run(job: InputSchema, cfg: dict = None) -> str:
    logger.info(f'Running job with input: {job}')
    api_key = os.getenv("OPENAI_API_KEY", None)

    if api_key is None:
        raise ValueError("OpenAI API key is not set")
    
    openai.api_key = api_key

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT.format(points="\n".join(job.points))},
    ]

    response = openai.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
    )

    description = response.choices[0].message.content
    
    if job.output_path:
        p = f"{job.output_path}/{DEAULT_FILENAME}"
        with open(p, "w") as f:
            f.write(description)

    return description


if __name__ == "__main__":
    input_data = {
        "points": ["Loves to travel", "Enjoys reading", "Loves to cook"]
    }
    job = InputSchema(**input_data)
    print(run(job))