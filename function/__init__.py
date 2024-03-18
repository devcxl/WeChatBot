from function.current_time_function import CurrentTimeFunction
from function.factory import Functions
from function.weather_function import WeatherFunction

functions = Functions()

functions.register(WeatherFunction)
functions.register(CurrentTimeFunction)

function_declares = functions.get_all_declare()

available_functions = functions.get_all_available()
