import requests


def get_current_weather(function_args):
    """Get the current weather in a given location"""
    location = function_args.get("location")
    GDKEY = 'b07a3300faadd38f99f1b10b0f9d9a25'
    weather_resp = requests.get(f'https://restapi.amap.com/v3/weather/weatherInfo?key={GDKEY}&city={location}&extensions=all')
    return weather_resp.text


function_list = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    }
]

available_functions = {
    'get_current_weather': get_current_weather
}
