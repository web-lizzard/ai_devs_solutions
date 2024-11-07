from openai import OpenAI
from langfuse import Langfuse
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

from langfuse.openai import OpenAI


client_with_observability = OpenAI()

langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    host=os.environ.get("LANGFUSE_HOST"),
)
