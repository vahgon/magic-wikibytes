from argparse import Namespace
from typing import Any, Self

from lib.parser._get_request import WikimediaRequest
from lib.util._set_env import EnvVars


class HTML:
    """
    Base class for the parsed wikitable. Holds raw wikimedia `Response` data.
    """
    def __init__(self, args: Namespace) -> None:
        self.USER_ARGS: Namespace       = args
        self._env_vars: EnvVars         = EnvVars()
        self._json:     dict[str, dict[str, str]]

        self.email:     str
        self.revid:     str
        self.request:   WikimediaRequest

    async def _async_init(self) -> Self:
        await self._env_vars
        self.revid = self._env_vars['REVID']
        u_arg_mail = self.USER_ARGS.email

        if u_arg_mail and u_arg_mail != self._env_vars['EMAIL']:
            self.email = await self._env_vars.change_val('EMAIL', u_arg_mail)
        else:
            self.email = self._env_vars['EMAIL']

        self.request = await WikimediaRequest(self.email, self.revid)

        return self

    async def check_duplicate_revid(self) -> bool:
        '''
        Checks whether the last execution of this script was given a response with a differing revision
        id than the current execution.
        '''
        if self.revid != self.request.raw_data:
            self.revid = await self._env_vars.change_val('REVID', self.request.raw_data)

        return False

    async def get_wikitable_req(self) -> str:
        """
        Make a request to the Wikimedia API specifying `text` as the content to be received
        in the response. This text holds the wikitable.

        :return: `str` value of the raw HTML in the Wikimedia response
        """
        self.request = await WikimediaRequest(self.email)

        return self.request.raw_data
