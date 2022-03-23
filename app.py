import os
from dotenv import load_dotenv

# We store the API key in the .env File in the format
# API_KEY = "THIS IS YOUR API KEY YOU GENERATED FROM CATO"
load_dotenv()
CATO_API_KEY = os.environ.get("API_KEY")
CATO_CUSTOMER = os.environ.get("CATO_CUSTOMER")