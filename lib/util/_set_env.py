from multiprocessing import Pool
from typing import Self, final

from lib.exceptions import MissingEnvValError
from lib.util.constants import ENV_PATH, ENV_VARS

try:
    from dotenv import get_key, set_key
except (ImportError, ModuleNotFoundError) as e:
    e.add_note("Could not find dotenv package -> pip install dotenv")
    raise e

async def _create_envfile() -> None:
    try:
        with open(file=ENV_PATH, mode='w', encoding='utf-8') as f:
            for k,v in ENV_VARS.items():
                f.write(f'{k}={v}\n')
    except IOError as e:
        raise e

@final
class EnvVars:
    """
    Gets/initializes/sets the environment variables set in 'lib/config/.conf' 
    """
    def __new__(cls) -> Self:
        if not hasattr(cls, 'init'):
            cls._obj = super().__new__(cls)
            setattr(cls, 'init', True)
        return cls._obj

    @classmethod
    async def _async_init(cls) -> Self:
        if not ENV_PATH.exists():
            await _create_envfile()

        with Pool(processes=2) as p:
            cls._val_dict = dict(zip(ENV_VARS.keys(), p.map(cls._get_var_val, ENV_VARS.items())))
            cls._null_req = [k for k, v in cls._val_dict.items() if v is None]

        for missing_key in cls._null_req:
            cls._set_init_val(missing_key)

        return cls._obj

    @classmethod
    def __await__(cls):
        return cls._async_init().__await__()

    @classmethod
    def __getitem__(cls, key: str) -> str:
        val = cls._val_dict.get(key)
        if val is None:
            raise MissingEnvValError(f"Invalid value found for {key} - value can not be NoneType")
        return val

    @staticmethod
    def _get_var_val(var: tuple[str, bool]) -> (str | None):
        key, required = var
        init_val = EnvVars._get_dotval(key)

        if required and (not init_val or init_val == ""):
            return None

        if not required and not init_val:
            set_key(ENV_PATH, key, "")

        return init_val

    @staticmethod
    def _get_dotval(key: str) -> (str | None):
        return get_key(ENV_PATH, key)

    @classmethod
    def _set_init_val(cls, key: str) -> None:
        val = input(f"Value missing from config: {key}\nPlease enter a value to use as {key}: ")
        set_key(
            dotenv_path=ENV_PATH,
            key_to_set=key,
            value_to_set=val
        )
        cls._val_dict[key] = val

    @classmethod
    async def change_val(cls, key: str, val: str) -> str:
        """
        Change the value of a specified key in the .conf dotenv file.

        :param key: `str` of dotenv variable to change.
        :param val: `str` of the value to be set.
        :return:    `str` of the passed value, now set for the specified env variable.
        """
        set_key(
            dotenv_path=ENV_PATH,
            key_to_set=key,
            value_to_set=str(val)
        )
        cls._val_dict[key] = val
        return val
