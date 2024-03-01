from function.factory import Functions

functions = Functions()

# functions.register(EmailFunction())
# functions.register(WeatherFunction())

function_declares = functions.get_all_declare()

available_functions = functions.get_all_available()
