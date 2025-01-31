import os
import dotenv
from openai import OpenAI, AzureOpenAI

from .Base import BaseModel
from utils.token_count import token_count
import anthropic
import os
import dotenv
dotenv.load_dotenv()
import time


class ClaudeModel(BaseModel):
    """
    Claude API Model interface
    
    Arguments
    ---------
    api_key : str
        Authentication token for the API. If not provided, looks for ANTHROPIC_API_KEY
    model_name : str
        Name of Claude model to use (default: claude-3-opus-20240229)
    temperature : float
        Temperature value (0.0-1.0), default 0.32
    max_tokens : int
        Maximum response tokens (default: 4096)
    """
    
    def __init__(
        self,
        api_key=None,
        model_name="claude-3-opus-20240229",
        temperature=0.32,
        max_tokens=4096,
        base_url=None,
    ):
        super().__init__()
        api_key = api_key or os.getenv("CLAUDE_API_KEY")
        assert api_key, "API Key required (ANTHROPIC_API_KEY environment variable)"
        
        self.client = anthropic.Anthropic(api_key=api_key)
        
        self.model_params = {
            "model": model_name,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

    def summarize_response(self, response):
        """Extracts Claude's response text"""
        if response.content and isinstance(response.content, list):
            return response.content[0].text
        return response

    def prompt(self, processed_input: list[dict]):
        """
        Claude API implementation
        
        Arguments
        ---------
        processed_input : list
            List of message dictionaries with "role" and "content"
            
        Returns
        -------
        response : tuple
            (content, input_tokens, output_tokens)
        """
        time.sleep(10)
        response = self.client.messages.create(
            messages=processed_input,
            **self.model_params
        )
        
        content = self.summarize_response(response)
        return (
            content,
            response.usage.input_tokens,
            response.usage.output_tokens
        )

class ClaudeSonnet(ClaudeModel):
    def prompt(self, processed_input: list[dict]):
        self.model_params["model"] = "claude-3-5-sonnet-20241022"
        return super().prompt(processed_input)

class ClaudeHaiku(ClaudeModel):
    def prompt(self, processed_input: list[dict]):
        self.model_params["model"] = "claude-3-5-haiku-20241022"
        return super().prompt(processed_input)