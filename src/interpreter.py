import discord
import asyncio

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.client = discord.Client()

    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, stmt):
        if stmt[0] == 'Set':
            self.variables[stmt[1]] = stmt[2]
        elif stmt[0] == 'Const':
            self.variables[stmt[1]] = stmt[2]
        elif stmt[0] == 'Function':
            self.functions[stmt[1]] = (stmt[2], stmt[3])
        elif stmt[0] == 'If':
            condition, body = stmt[1], stmt[2]
            if self.evaluate(condition):
                for s in body:
                    self.execute(s)
        elif stmt[0] == 'Repeat':
            condition, body = stmt[1], stmt[2]
            while self.evaluate(condition):
                for s in body:
                    self.execute(s)
        elif stmt[0] == 'Print':
            print(self.evaluate(stmt[1]))
        elif stmt[0] == 'Send':
            channel = self.evaluate(stmt[2])
            message = self.evaluate(stmt[1])
            asyncio.run_coroutine_threadsafe(self.send_message(channel, message), self.client.loop)
        elif stmt[0] == 'StartBot':
            token = self.evaluate(stmt[1])
            asyncio.run(self.start_bot(token))

    def evaluate(self, expr):
        if isinstance(expr, int):
            return expr
        elif expr in self.variables:
            return self.variables[expr]
        else:
            return expr

    async def start_bot(self, token):
        @self.client.event
        async def on_ready():
            if 'onReady' in self.functions:
                await self.execute_function('onReady', [])

        @self.client.event
        async def on_message(message):
            if 'onMessage' in self.functions:
                await self.execute_function('onMessage', [message])

        await self.client.start(token)

    async def send_message(self, channel_name, message):
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                if channel.name == channel_name:
                    await channel.send(message)
                    return
        raise ValueError(f"Channel {channel_name} not found")

    async def execute_function(self, func_name, args):
        params, body = self.functions[func_name]
        old_vars = self.variables.copy()
        self.variables.update(zip(params, args))
        for stmt in body:
            self.execute(stmt)
        self.variables = old_vars
