from .command_factory import CommandFactory
from .emoji_command import EmojiCommand
from .group_command import GroupCommand
from .weather_command import WeatherCommand
from .weibo_command import WeiboCommand
from .tts_command import TTSCommand
from .vits_command import VITSCommand

factory = CommandFactory()
factory.registerCommand(WeatherCommand())
factory.registerCommand(GroupCommand())
factory.registerCommand(EmojiCommand())
factory.registerCommand(WeiboCommand())
factory.registerCommand(TTSCommand())
factory.registerCommand(VITSCommand())
