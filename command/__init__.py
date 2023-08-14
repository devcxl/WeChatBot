from .command_factory import CommandFactory
from .emoji_command import EmojiCommand
from .group_command import GroupCommand
from .weather_command import WeatherCommand
from .weibo_command import WeiboCommand
from .tts_command import TTSCommand

factory = CommandFactory()
factory.registerCommand(WeatherCommand())
factory.registerCommand(GroupCommand())
factory.registerCommand(EmojiCommand())
factory.registerCommand(WeiboCommand())
factory.registerCommand(TTSCommand())
