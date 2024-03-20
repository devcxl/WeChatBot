import os

api_url = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1')
api_keys = os.getenv('OPENAI_API_KEYS').split(',')
default_prompt = os.getenv('DEFAULT_PROMPT', 'You are a helpful assistant.')
model = os.getenv('MODEL', 'gpt-3.5-turbo')
history = os.getenv('HISTORY', 15)
data_dirs = os.getenv('DATA_DIR', '/data')
proxy = os.getenv('OPENAI_PROXY')
debug = os.getenv('DEBUG_MODE', False)
dalle3_cache = os.getenv('OPENAI_DALL-E3_CACHE', True)
