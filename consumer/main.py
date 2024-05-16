from dotenv import load_dotenv
from starter import Starter


def app():
    # Loading .env
    load_dotenv()

    # Starting consumer
    Starter().start()


if __name__ == "__main__":
    app()
