from typing import List
import tiktoken
import os
import copy
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from models.Base import BaseModel
from datasets.Dataset import Dataset
from results.Results import Results
from utils.parse import parse_response
from tqdm import tqdm
import logging
from typing import Union, List
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class BaseStrategy(object):
    def __init__(
        self,
        model: Union[BaseModel, List[BaseModel]],
        data: Dataset,
        language: str,
        pass_at_k: int,
        results: Results,
        verbose: bool = True,
    ):
        self.model = model
        self.data = data
        self.pass_at_k = pass_at_k
        self.results = results
        self.language = language
        self.verbose = verbose
        self.results_lock = Lock()

    def gpt_chat(self, processed_input: List[dict], index: int=0) -> (str, int, int):
        if isinstance(self.model, list):
            return self.model[index].prompt(processed_input=processed_input)
        else:
            return self.model.prompt(processed_input=processed_input)

    def run_single_pass(self, item: dict):
        pass

    def process_item(self, args):
        i, item = args
        num_items = len(self.data)
        
        if i < len(self.results):
            item = copy.deepcopy(self.results[i])
            cur_pass = len(item["source_codes"])
            is_solved = item["is_solved"]
            cur_imp = item["source_codes"][-1]
        else:
            item = copy.deepcopy(item)
            item["source_codes"] = []
            item["responses"] = []
            item["prompt_tokens"] = []
            item["completion_tokens"] = []
            item["no_of_try"] = 0
            cur_pass = 0
            is_solved = False
            cur_imp = ""

        while cur_pass < self.pass_at_k and not is_solved:
            try:
                response, prompt_tokens, completion_tokens = self.run_single_pass(item)
                if hasattr(self, "parse_code"):
                    cur_imp = self.parse_code(response)
                else:
                    cur_imp = parse_response(response)

                item["source_codes"].append(cur_imp)
                item["responses"].append(response)
                item["prompt_tokens"].append(prompt_tokens)
                item["completion_tokens"].append(completion_tokens)
                item["no_of_try"] += 1

                is_solved = self.data.evaluate(
                    item=item,
                    cur_imp=cur_imp,
                    language=self.language
                )
            except Exception as e:
                logger.error(f"An error occurred: {e}")
            finally:
                cur_pass += 1

        item["is_solved"] = is_solved
        item["language"] = self.language
        
        return i, item, is_solved

    def run(self):
        num_items = len(self.data)
        num_success = 0
        max_workers = 8
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Start from last finished index
            start_idx = len(self.results)
            # Submit remaining tasks
            future_to_idx = {
                executor.submit(self.process_item, (i, item)): i 
                for i, item in enumerate(self.data[start_idx:], start=start_idx)
            }
            
            # Process results as they complete
            num_complete = 0
            for future in tqdm(as_completed(future_to_idx), total=num_items-start_idx):
                num_complete += 1
                i, item, is_solved = future.result()
                if is_solved:
                    num_success += 1
                
                with self.results_lock:
                    self.results.results.append(item)
                    self.results.save_results()
                
                if self.verbose:
                    with open('./outputs/Final_Result.txt', 'a') as f:
                        print(f'completed {i+1}, {num_complete}/{num_items}, Solved: {is_solved}, number of success = {num_success}, acc = {num_success}/{num_complete}, {round(num_success/(num_complete)*100, 2)}', file=f)

        num_success = [item["is_solved"] for item in self.results.results]
        with open('./outputs/Final_Result.txt', 'a') as f:
            print('completed, ', sum(num_success), '/', num_items, '=', round(sum(num_success)/num_items*100, 2), '%', file=f)
