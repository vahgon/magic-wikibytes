import os
from pathlib import Path

from lib.exceptions import MissingEnvValError, MissingEnvVarError
from lib.util.constants import ENV_PATH, USER_ARGS

try:
    import dotenv
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("Install dotenv -> pip install dotenv")
    raise e

email: (str | None) = USER_ARGS.email if USER_ARGS.email != '' else None

def _create_envfile() -> None:
    try:
        with open(file=ENV_PATH, mode='w') as f:
            f.write(f'EMAIL={email}')
            f.close()
    except OSError as e:
        raise e

def _check_email_env() -> None:
    global email
    envVars = dotenv.dotenv_values(ENV_PATH)

    try:
        email = envVars['EMAIL'] if envVars['EMAIL'] != '' else None
    except MissingEnvVarError as e:
        e.add_note(f'Error when parsing {ENV_PATH} - no "EMAIL" variable found.')
        os.remove(ENV_PATH)
        raise e

def _check_conf_change(key: str, val: str) -> None:
    dotenv.set_key(dotenv_path=ENV_PATH, key_to_set=key, value_to_set=val)

def get_email() -> str:
    if not Path(ENV_PATH).exists():
        _create_envfile()
    elif email is None:
        _check_email_env()
    elif email:
        _check_conf_change('EMAIL', email)

    if not isinstance(email, str):
        raise MissingEnvVarError()

    return email
