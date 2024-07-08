import re

class Tokenizer:
    def __init__(self, code):
        self.tokens = re.findall(r'\w+|".*?"|\S', code)
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
