import re
import multiprocessing

"""
Retriving the code blocks from the response.
"""
def parse_response(response: str) -> str:
    # print("===============response in parse response=============", response, "\n")

    if "```" not in response:
        return response

    code_pattern = r'```((.|\n)*?)```'
    if "```Python" in response:
        code_pattern = r'```Python((.|\n)*?)```'
    if "```Python3" in response:
        code_pattern = r'```Python3((.|\n)*?)```'
    if "```python" in response:
        code_pattern = r'```python((.|\n)*?)```'
    if "```python3" in response:
        code_pattern = r'```python3((.|\n)*?)```'
    if "```C" in response:
        code_pattern = r'```C((.|\n)*?)```'
    if "```c" in response:
        code_pattern = r'```c((.|\n)*?)```'
    if "```C++" in response:
        code_pattern = r'```C\+\+((.|\n)*?)```'
    if "```c++" in response:
        code_pattern = r'```c\+\+((.|\n)*?)```'
    if "```cpp" in response:
        code_pattern = r'```cpp((.|\n)*?)```'
    if "```Cpp" in response:
        code_pattern = r'```Cpp((.|\n)*?)```'
    if "```Java" in response:
        code_pattern = r'```Java((.|\n)*?)```'
    if "```java" in response:
        code_pattern = r'```java((.|\n)*?)```'
    if "```Node" in response:
        code_pattern = r'```Node((.|\n)*?)```'
    if "```node" in response:
        code_pattern = r'```node((.|\n)*?)```'
    if "```Rust" in response:
        code_pattern = r'```Rust((.|\n)*?)```'
    if "```rust" in response:
        code_pattern = r'```rust((.|\n)*?)```'
    if "```PHP" in response:
        code_pattern = r'```PHP((.|\n)*?)```'
    if "```php" in response:
        code_pattern = r'```php((.|\n)*?)```'
    if "```Go" in response:
        code_pattern = r'```Go((.|\n)*?)```'
    if "```go" in response:
        code_pattern = r'```go((.|\n)*?)```'
    if "```Ruby" in response:
        code_pattern = r'```Ruby((.|\n)*?)```'
    if "```ruby" in response:
        code_pattern = r'```ruby((.|\n)*?)```'
    if "```C#" in response:
        code_pattern = r'```C#((.|\n)*?)```'
    if "```c#" in response:
        code_pattern = r'```c#((.|\n)*?)```'
    if "```csharp" in response:
        code_pattern = r'```csharp((.|\n)*?)```'

    # Wrap the re.findall call using multiprocessing
    def find_code_blocks(queue):
        result = re.findall(code_pattern, response, re.DOTALL)
        queue.put(result)

    default_value = response
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=find_code_blocks, args=(queue,))
    process.start()
    process.join(timeout=30)  # Wait for up to 10 seconds

    if process.is_alive():
        process.terminate()
        process.join()
        print("============multiprocessing time out error in parse_response==============")
        return default_value  # Return default value if timeout occurs
    else:
        if not queue.empty():
            code_blocks = queue.get()
        else:
            return default_value
    
    if not code_blocks:
        return response
    
    if type(code_blocks[-1]) == tuple or type(code_blocks[-1]) == list:
        code_str = "\n".join(code_blocks[-1])
    elif type(code_blocks[-1]) == str:
        code_str = code_blocks[-1]
    else:
        code_str = response

    return code_str

"""
Taking plan in numbered list format and return the list of plans.
Exmaple:
Input:
1. Plan A
2. Plan B
3. Plan C
Output: ["Plan A", "Plan B", "Plan C"]
"""
def extract_plans(planing: str) -> list[str]:
    plans = []
    for line in planing.strip().split("\n"):
        splits = line.split(". ")
        if len(splits) < 2:
            continue
        if splits[0].isnumeric():
            plans.append(splits[1])

    return plans