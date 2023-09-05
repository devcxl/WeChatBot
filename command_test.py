from command import factory

user = {}


def emoji_test():
    executor = factory.getCommand('/emoji')
    print(executor.execute(user, ['/emoji']))
    print(executor.execute(user, ['/emoji', 'set_rate', '30']))
    print(executor.execute(user, ['/emoji', 'set_rate', 'A']))
    print(executor.execute(user, ['/emoji', 'install', 'bilibili']))
    print(executor.execute(user, ['/emoji', 'install', 'bilibili', '-f']))


def tts_test():
    tts = factory.getCommand('/tts')
    tts.execute(user, ['/tts', '我要给你完整的童年。'])


def weibo_test():
    weibo_hot = factory.getCommand('/weibo')
    weibo_hot.execute(user, ['/weibo'])


def weather_test():
    weather = factory.getCommand('/weather')
    weather.execute(user, ['/weather', '北京'])


if __name__ == "__main__":
    pass
