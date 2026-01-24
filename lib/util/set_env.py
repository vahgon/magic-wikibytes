from lib.exceptions import MissingEnvError
from pathlib import Path
from lib.constants import ROOT
import pathlib

try:
    import dotenv
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("Install dotenv -> pip install dotenv")
    raise e

env_path = Path(str(ROOT) + "/.conf")
email = ''

def ask_user_input() -> str:
    return input("Please provide an email address to use when making requests to the wikipedia API: ")

def create_dotenv() -> None:
    try:
        with open(env_path, "w") as f:
            _ = f.write("EMAIL=" + ask_user_input())
    except Exception as e:
        e.add_note("Error when attempting to open env_path")
        raise

def check_dotenv_file() -> None:
    if not pathlib.Path(env_path).exists():
        try:
            create_dotenv()
        except Exception as e:
            e.add_note("Error creating dotenv file")

    check_env_val()

def check_env_val() -> None:
    global email
    env_val = dotenv.dotenv_values(env_path)
    check_env_email = ""

    try:
        check_env_email = env_val['EMAIL'] if env_val['EMAIL'] is not None else None
    except MissingEnvError:
        with open(env_path, "w") as f:
            _ = f.write("EMAIL=")

    email = check_env_email
    if email is None or email == "":
        try:
            with open(env_path, "w") as f:
                set_usr_email = "EMAIL=" + ask_user_input()
                _ = f.write(set_usr_email)
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

