# My Language Project

This project is a simple programming language designed to be easy to understand and use, even for beginners.

## Structure

- `src/`: Contains the source code for the language.
- `tests/`: Contains the test cases.
- `examples/`: Contains example programs written in the new language.

## How to Run

To run the interpreter, use the following command:

```sh
python src/main.py examples/example_code.txt
```

### Step 3: Fill Out the Requirements

If you have any dependencies, add them to `requirements.txt`. For now, you might not need any.

### Step 4: Implement the Tokenizer

Let's start with the `src/tokenizer.py`:

```python
import re

class Tokenizer:
    def __init__(self, code):
        self.tokens = re.findall(r'[a-zA-Z]+|\d+|[=+*()-]', code)
        self.position = 0

    def next_token(self):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return None

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
```
