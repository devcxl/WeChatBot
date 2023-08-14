from .command_factory import CommandFactory
from .emoji_command import EmojiCommand
from .group_command import GroupCommand
from .weather_command import WeatherCommand
from .weibo_command import WeiboCommand

factory = CommandFactory()
factory.registerCommand(WeatherCommand())
factory.registerCommand(GroupCommand())
factory.registerCommand(EmojiCommand())
factory.registerCommand(WeiboCommand())
