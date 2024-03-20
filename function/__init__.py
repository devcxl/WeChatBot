from function.current_time_function import CurrentTimeFunction
from function.email_send_function import EmailFunction
from function.factory import Functions
from function.weather_function import WeatherFunction
from function.web_search_function import WebSearchFunction

functions = Functions()

functions.register(WeatherFunction)
functions.register(CurrentTimeFunction)
functions.register(EmailFunction)
functions.register(WebSearchFunction)

function_declares = functions.get_all_declare()

available_functions = functions.get_all_available()
