class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        statements = []
        while (token := self.tokenizer.peek()) is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.tokenizer.next_token()
        if token == 'Set':
            return self.parse_assignment()
        elif token == 'Const':
            return self.parse_constant()
        elif token == 'Define':
            return self.parse_function()
        elif token == 'If':
            return self.parse_if()
        elif token == 'Repeat':
            return self.parse_repeat()
        elif token == 'Print':
            return self.parse_print()
        elif token == 'Send':
            return self.parse_send()
        elif token == 'Start':
            return self.parse_start_bot()
        else:
            raise SyntaxError(f"Unknown statement: {token}")

    def parse_assignment(self):
        var_name = self.tokenizer.next_token()
        if self.tokenizer.next_token() != 'to':
            raise SyntaxError("Expected 'to' after variable name")
        value = self.tokenizer.next_token()
        return ('Set', var_name, self.parse_expression(value))

    def parse_constant(self):
        var_name = self.tokenizer.next_token()
        if self.tokenizer.next_token() != '=':
            raise SyntaxError("Expected '=' after constant name")
        value = self.tokenizer.next_token()
        return ('Const', var_name, self.parse_expression(value))

    def parse_function(self):
        func_name = self.tokenizer.next_token()
        if self.tokenizer.peek() == 'with':
            self.tokenizer.next_token()
            params = [self.tokenizer.next_token()]
        else:
            params = []
        self.tokenizer.next_token()  # consume 'End'
        body = []
        while (token := self.tokenizer.peek()) != 'End':
            body.append(self.parse_statement())
        self.tokenizer.next_token()  # consume 'End'
        return ('Function', func_name, params, body)

    def parse_if(self):
        condition = self.parse_expression(self.tokenizer.next_token())
        self.tokenizer.next_token()  # consume 'then'
        body = []
        while (token := self.tokenizer.peek()) != 'End':
            body.append(self.parse_statement())
        self.tokenizer.next_token()  # consume 'End'
        return ('If', condition, body)

    def parse_repeat(self):
        if self.tokenizer.next_token() != 'while':
            raise SyntaxError("Expected 'while' after 'Repeat'")
        condition = self.parse_expression(self.tokenizer.next_token())
        body = []
        while (token := self.tokenizer.peek()) != 'End':
            body.append(self.parse_statement())
        self.tokenizer.next_token()  # consume 'End'
        return ('Repeat', condition, body)

    def parse_print(self):
        value = self.parse_expression(self.tokenizer.next_token())
        return ('Print', value)

    def parse_send(self):
        message = self.parse_expression(self.tokenizer.next_token())
        self.tokenizer.next_token()  # consume 'to'
        channel = self.parse_expression(self.tokenizer.next_token())
        return ('Send', message, channel)

    def parse_start_bot(self):
        self.tokenizer.next_token()  # consume 'bot'
        self.tokenizer.next_token()  # consume 'with'
        token = self.parse_expression(self.tokenizer.next_token())
        return ('StartBot', token)

    def parse_expression(self, token):
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]  # Remove quotes from string literals
        try:
            return int(token)
        except ValueError:
            return token  # Return as variable name or function name
