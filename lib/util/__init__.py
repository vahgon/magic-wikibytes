from lib.util._logger import log

from lib.util.constants import(
    ReqJson,            # noqa: F401
    HtmlJson,           # noqa: F401
    ColType,            # noqa: F401
    FileData,            # noqa: F401
    USER_ARGS,          # noqa: F401
    DOCS_PATH,          # noqa: F401
    ROOT,               # noqa: F401
)

from lib.util._set_env import get_email
EMAIL: str = get_email()
