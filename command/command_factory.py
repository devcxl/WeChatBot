from .base_command import BaseCommand


class CommandFactory():
    '''命令工厂'''

    def __init__(self) -> None:
        self.commands = {}

    def registerCommand(self, command: BaseCommand) -> None:
        self.commands[command.getCommandName()] = command

    def getCommand(self, commandName) -> BaseCommand:
        command = self.commands.get(commandName)
        if command is None:
            raise ValueError(f"Unknown command: {commandName}")
        return command
