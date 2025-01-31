from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def get_scores(coding_problem):
    prompt = f"""
    Evaluate the given coding task based on the following criteria and provide only a final list of scores in order (separated by spaces), without explanations. Use the scoring system provided below:

    1. Algorithm Complexity (1-5)
    2. Edge Case Sensitivity (1-5)
    3. Optimality Gap (1-5)
    4. Spatial Reasoning (1-5)
    5. Implementation Pitfalls (1-5)
    6. Test Case Complexity (1-5)
    7. Cognitive Load (1-5)
    8. Domain Knowledge (1-5)

    ### Scoring Guide:
    - **1 (Simple Task - Default Choice):** Straightforward logic, minimal complexity, no special considerations (e.g., basic operations, a single loop, or a direct formula).  
    - **3 (Moderate Complexity - Only if Necessary):** Some level of nested operations, basic optimization opportunities, or simple edge cases.  
    - **5 (Complex - Rare Cases Only):** Advanced algorithmic knowledge, multiple failure points, or intricate logic requiring deep expertise.  
    
    ⚠️**Unless the task clearly requires complex reasoning, default to the lowest reasonable score (1).**  
    ⚠️ **Most tasks should be simple (favor lower scores unless there is strong justification for complexity).**
--------------------
    ### **Example Task (Simple Case):**

    ```python
    from typing import List

    def has_close_elements(numbers: List[float], threshold: float) -> bool:
        "Check if in given list of numbers, are any two numbers closer to each other than
        given threshold.
        >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
        False
        >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
        True
        "
    ```
    Example Task Scores (Adjusted for Simplicity):
        •	Algorithm Complexity: 2 (Basic pairwise comparison, though O(n²), straightforward)
        •	Edge Case Sensitivity: 1 (Few edge cases, easy to handle)
        •	Optimality Gap: 2 (Optimization possible but not crucial)
        •	Spatial Reasoning: 2 (Simple numerical comparison)
        •	Implementation Pitfalls: 2 (Minimal risk of errors)
        •	Test Case Complexity: 2 (Only basic floating point precision concerns)
        •	Cognitive Load: 2 (No major state tracking needed)
        •	Domain Knowledge: 1 (Requires no special algorithm knowledge)

    Example Output (Favoring Simplicity):
    2 1 2 2 2 2 2 1
-------------------------
    Now, provide the scores for the given coding task.

    {coding_problem}
    """

    client = OpenAI(api_key=openai_api_key, timeout=60*5)

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ]
    )
    
    
    
    # return completion.choices[0].message.content.strip('"')
    return completion.choices[0].message.content

def get_complexity(coding_problem):
    res = get_scores(coding_problem)
    int_list = list(map(int, res.split()))
        
    score = sum(int_list) / len(int_list) / 8
    
    if score < 0.33:
        return "simple"
    elif score > 0.33 and score < 0.66:
        return "moderate"
    elif score > 0.66:
        return "complex"
    return 0    
