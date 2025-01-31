from test_complexity import get_complexity

import sys
from datetime import datetime
from constants.paths import *

from models.Gemini import Gemini
from models.OpenAI import OpenAIModel

from results.Results import Results

from promptings.PromptingFactory import PromptingFactory
from datasets.DatasetFactory import DatasetFactory
from models.ModelFactory import ModelFactory

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dataset", 
    type=str, 
    default="HumanEval", 
    choices=[
        "HumanEval", 
        "MBPP", 
        "APPS",
        "xCodeEval", 
        "CC", 
    ]
)
parser.add_argument(
    "--strategy", 
    type=str, 
    default="MapCoder", 
    choices=[
        "Direct",
        "CoT",
        "SelfPlanning",
        "Analogical",
        "MapCoder",
    ]
)
parser.add_argument(
    "--model", 
    type=str, 
    default="ChatGPT", 
    choices=[
        "ChatGPT",
        "GPT4",
        "Gemini",
        "Llama31_8B",
        "Llama31_70B",
        "Llama31_8B_Groq",
        "Llama31_70B_Groq",
        "Llama31_8B_Novita",
        "Llama31_70B_Novita",
        "Qwen2_7B_Novita",
        "Qwen2_72B_Novita",
        "ClaudeSonnet",
        "ClaudeHaiku",
        "GPT4o",
        "GPT4oMini",
        "DeepSeekV3",
        "DeepSeekR1",
    ],
    nargs='+'
)
parser.add_argument(
    "--temperature", 
    type=float, 
    default=0
)
parser.add_argument(
    "--pass_at_k", 
    type=int, 
    default=1
)
parser.add_argument(
    "--language", 
    type=str, 
    default="Python3", 
    choices=[
        "C",
        "C#",
        "C++",
        "Go",
        "PHP",
        "Python3",
        "Ruby",
        "Rust",
    ]
)

parser.add_argument(
    "--base_url", 
    type=str, 
    default="https://api.openai.com/", 
    choices=[
        "http://localhost:8000/v1",
        "http://localhost:8002/v1",
        "https://api.openai.com/",
    ],
    nargs='+'
)

args = parser.parse_args()

assert isinstance(args.model, str) or (isinstance(args.model, list) and len(args.model) == 1) or (args.strategy == "MapCoder" and isinstance(args.model, list) and len(args.model) == 3), "Invalid number of models"

DATASET = args.dataset
STRATEGY = args.strategy
MODEL_NAME = " || ".join(args.model) if isinstance(args.model, list) else args.model

TEMPERATURE = args.temperature
PASS_AT_K = args.pass_at_k
LANGUAGE = args.language

RUN_NAME = f"{MODEL_NAME}-{STRATEGY}-{DATASET}-{LANGUAGE}-{TEMPERATURE}-{PASS_AT_K}"
RESULTS_PATH = f"./outputs/{RUN_NAME}.jsonl"

data=DatasetFactory.get_dataset_class(DATASET)()

for item in data:
    complexity = get_complexity(data.get_prompt(item))
    if complexity == "easy":
        model_name="GPT4oMini"
        strategy = "CoT"
    elif complexity == "medium":
        model_name="GPT4o"
        strategy = "CoT"    
    else:
        model_name="GPT4o"
        strategy = "MapCoder"    

    strategy = PromptingFactory.get_prompting_class(strategy)(model=ModelFactory.get_model_class(model_name=model_name,  kwargs_list = [{"base_url": url} for url in (args.base_url or [])],),
                                                            language=LANGUAGE,
                                                            pass_at_k=PASS_AT_K,
                                                            data=item,
                                                            results=Results(RESULTS_PATH),
                                                            verbose=True,)
strategy.run()        


