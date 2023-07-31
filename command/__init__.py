class BaseCommand():
    def __init__(self) -> None:
        pass
    def getCommand() -> str:
        raise NotImplementedError
    def execute(self, params=None) -> str:
        raise NotImplementedError
    
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


class RoleCommand(BaseCommand):
    '''角色命令'''

    def __init__(self) -> None:
        self.sub_commands = ['set','get']
        super().__init__()

    def getCommandName(self):
        return '/role'

    def execute(self, params=None):
        sub_command=params[0]
        if sub_command in self.sub_commands:
            if sub_command == 'set':
                pass
            elif sub_command == 'get':
                pass
        
        return "role command executed."


factory = CommandFactory()
factory.registerCommand(RoleCommand())