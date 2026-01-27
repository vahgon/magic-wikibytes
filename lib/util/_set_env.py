from lib.util.constants import ENV_PATH, USER_ARGS
from lib.exceptions import MissingEnvVarError, MissingEnvValError
from pathlib import Path
import os
  
try:
    import dotenv
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("Install dotenv -> pip install dotenv")
    raise e

email: str | None = USER_ARGS.email if USER_ARGS.email != '' else None

def _check_conf() -> str:
    if not Path(ENV_PATH).exists():
        _create_conf()
    return _check_environ_vars()

def _create_conf() -> None:
    toFileEmail = email if email else ''
    try:
        with open(file=ENV_PATH, mode='w') as f:
            _ = f.write(f'EMAIL={toFileEmail}')
            f.close()
    except OSError as e:
        raise e

def _check_environ_vars() -> str:
    envVars = dotenv.dotenv_values(ENV_PATH)
    checkEnvEmail: str | None = None
    try:
        checkEnvEmail = envVars['EMAIL'] if envVars['EMAIL'] != '' else None
    except MissingEnvVarError as e:
        e.add_note(f'Error when parsing {ENV_PATH} - no "EMAIL" variable found.')
        os.remove(ENV_PATH)
        raise e

    return _possible_results(checkEnvEmail)

def _change_conf_val(key: str, val: str, oldVal: str | None) -> None:
    if USER_ARGS.verbose and oldVal is None:
        print(f'Adding provided email "{email}" to .conf')
    elif USER_ARGS.verbose and isinstance(oldVal, str):
        print(f'Provided email does not match what is located in .conf. Changing {oldVal} to {email}')

    _ = dotenv.set_key(dotenv_path=ENV_PATH, key_to_set=key, value_to_set=val)

def _possible_results(envMail: str | None) -> str:
    match envMail, email:
        case str(), str():
            _change_conf_val('EMAIL', email, envMail)
            return email
        case None, str():
            _change_conf_val('EMAIL', email, envMail)
            return email
        case str(), None:
            return envMail
        case None, None:
            e = MissingEnvValError()
            e.add_note("Email is not set in .conf - Please set it when making requests to wiki API!")
            raise e

def get_email() -> str:
    return _check_conf()
