from dotenv import load_dotenv
from consumer.starter import Starter

if __name__ == "__main__":
    # Loading .env
    load_dotenv()

    # Starting consumer
    Starter()

