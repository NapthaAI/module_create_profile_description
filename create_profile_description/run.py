from dotenv import load_dotenv
from litellm import completion
import os
import yaml
from create_profile_description.schemas import InputSchema
from create_profile_description.utils import get_logger

load_dotenv()
logger = get_logger(__name__)

def run(inputs: InputSchema, cfg: dict = None) -> str:
    logger.info(f'Running job with inputs: {inputs}')
    
    messages = [
        {"role": "system", "content": cfg["inputs"]["system_message"]},
        {"role": "user", "content": cfg["inputs"]["user_prompt"].format(points="\n".join(inputs.points))},
    ]

    response = completion(
        model=cfg["models"]["ollama"]["model"],
        messages=messages,
        max_tokens=cfg["models"]["ollama"]["max_tokens"],
        temperature=cfg["models"]["ollama"]["temperature"],
        api_base=cfg["models"]["ollama"]["api_base"],
    )

    description = response.choices[0].message.content
    
    logger.info(f"Description: {description}")

    if inputs.output_path:
        p = f"{inputs.output_path}/{cfg["outputs"]["filename"]}"
        with open(p, "w") as f:
            f.write(description)

    return description


if __name__ == "__main__":
    cfg_path = f"create_profile_description/component.yaml"
    with open(cfg_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    input_data = {
        "points": ["Loves to travel", "Enjoys reading", "Loves to cook"]
    }
    inputs = InputSchema(**input_data)
    print(run(inputs, cfg))