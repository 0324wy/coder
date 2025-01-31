from typing import Union, List
from models.Gemini import Gemini
from models.OpenAI import ChatGPT, GPT4, GPT4o, GPT4oMini
from models.OpenSource import Llama31_8B, Llama31_70B
from models.OpenSourceGorq import Llama31_8B_Groq, Llama31_70B_Groq
from models.OpenSourceNovita import Llama31_8B_Novita, Llama31_70B_Novita, Qwen2_72B_Novita, Qwen2_7B_Novita, DeepSeekR1
from models.Claude import ClaudeHaiku, ClaudeSonnet

class ModelFactory:
    def _get_model_class(model_name: str):
        if model_name == "Gemini":
            return Gemini
        elif model_name == "ChatGPT":
            return ChatGPT
        elif model_name == "GPT4":
            return GPT4
        elif model_name == "GPT4o":
            return GPT4o
        elif model_name == "GPT4oMini":
            return GPT4oMini
        elif model_name == "Llama31_8B":
            return Llama31_8B
        elif model_name == "Llama31_70B":
            return Llama31_70B
        elif model_name == "Llama31_8B_Groq":
            return Llama31_8B_Groq
        elif model_name == "Llama31_70B_Groq":
            return Llama31_70B_Groq
        elif model_name == "Llama31_8B_Novita":
            return Llama31_8B_Novita
        elif model_name == "Llama31_70B_Novita":
            return Llama31_70B_Novita
        elif model_name == "Qwen2_72B_Novita":
            return Qwen2_72B_Novita
        elif model_name == "Qwen2_7B_Novita":
            return Qwen2_7B_Novita
        elif model_name == "ClaudeSonnet":
            return ClaudeSonnet
        elif model_name == "ClaudeHaiku":
            return ClaudeHaiku    
        elif model_name == "DeepSeekR1":
            return DeepSeekR1                 
        else:
            raise Exception(f"Unknown model name {model_name}")
        
    # @staticmethod
    # def get_model_class(model_name: Union[str, List[str]], **kwargs):
    #     if isinstance(model_name, list):
    #         if len(model_name) == 1:
    #             return ModelFactory._get_model_class(model_name[0])(**kwargs)
    #         return [ModelFactory._get_model_class(model)(**kwargs) for model in model_name]
    #     else:
    #         return ModelFactory._get_model_class(model_name)(**kwargs)

    @staticmethod
    def get_model_class(model_name: Union[str, List[str]], kwargs_list=None, **kwargs):
        """
        Returns the class or instances of the specified model(s), combining common and specific keyword arguments.
        
        Args:
            model_name (Union[str, List[str]]): A single model name or a list of model names.
            kwargs_list (List[dict], optional): A list of keyword arguments for each model. 
                                                Must match the length of model_name if provided.
            **kwargs: Common keyword arguments to apply to all models.
        
        Returns:
            A single model instance or a list of model instances.
        
        Raises:
            ValueError: If model_name is a list and the length of kwargs_list doesn't match.
        """
        # print(kwargs_list)
        # print(**kwargs)
        if isinstance(model_name, list) and len(model_name) > 1:
            if kwargs_list is None or len(kwargs_list) == 0:
                kwargs_list = [{}] * len(model_name)  # Default: empty dict for each model
            
            # if len(model_name) != len(kwargs_list):
            #     raise ValueError("Length of model_name and kwargs_list must match.")
            
            # Merge common kwargs with individual kwargs for each model
            return [
                ModelFactory._get_model_class(model)(**{**kwargs, **kwargs_list[i]})
                for i, model in enumerate(model_name)
            ]
        else:
            # Single model case: use only common kwargs
            return ModelFactory._get_model_class(model_name[0])(**{**kwargs, **kwargs_list[0]})