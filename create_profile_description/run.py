from dotenv import load_dotenv
from litellm import completion
import os
from create_profile_description.schemas import InputSchema
from naptha_sdk.utils import get_logger, load_yaml
from typing import Dict

load_dotenv()
logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes = None, orchestrator_node = None, flow_run = None, cfg: Dict = None) -> str:
    logger.info(f'Running module with inputs: {inputs}')
    
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
    cfg = load_yaml(cfg_path)

    input_data = {
        "points": ["Loves to travel", "Enjoys reading", "Loves to cook"]
    }
    inputs = InputSchema(**input_data)
    print(run(inputs, cfg=cfg))