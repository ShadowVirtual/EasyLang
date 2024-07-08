import sys
from tokenizer import Tokenizer
from my_parser import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) != 3:
        print("Usage: python src/main.py <script_file> <discord_token>")
        sys.exit(1)

    script_file = sys.argv[1]
    discord_token = sys.argv[2]

    with open(script_file, 'r') as file:
        code = file.read()

    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    statements = parser.parse()
    interpreter = Interpreter()
    interpreter.variables['botToken'] = discord_token  # Set the bot token
    interpreter.interpret(statements)

if __name__ == '__main__':
    main()
