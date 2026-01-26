from lib.exceptions import MissingEnvError
from lib.constants import ENV_PATH
import pathlib

try:
    import dotenv
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("Install dotenv -> pip install dotenv")
    raise e

email = ''

def ask_user_input() -> str:
    return input("Please provide an email address to use when making requests to the wikipedia API: ")

def create_dotenv() -> None:
    try:
        with open(ENV_PATH, "w") as f:
            _ = f.write("EMAIL=" + ask_user_input())
    except Exception as e:
        e.add_note("Error when attempting to open env_path")
        raise

def check_dotenv_file() -> None:
    if not pathlib.Path(ENV_PATH).exists():
        try:
            create_dotenv()
        except Exception as e:
            e.add_note("Error creating dotenv file")

    check_env_val()

def check_env_val() -> None:
    global email
    envVal = dotenv.dotenv_values(ENV_PATH)
    checkEnvEmail = ""

    try:
        checkEnvEmail = envVal['EMAIL'] if envVal['EMAIL'] is not None else None
    except MissingEnvError:
        with open(ENV_PATH, "w") as f:
            _ = f.write("EMAIL=")

    email = checkEnvEmail
    if email is None or email == "":
        try:
            with open(ENV_PATH, "w") as f:
                setUserEmail = "EMAIL=" + ask_user_input()
                _ = f.write(setUserEmail)
        except Exception as e:
            raise e

    if email is not None or "":
        pass
    else:
        e = MissingEnvError()
        e.add_note(".env exists, but email is blank. Please set it before sending requests to the API")
        raise e

def get_email() -> str | None:
    check_dotenv_file()
    return email
