import asyncio
import json
import logging
import os
import typing as t
import sys

import discord
from discord.ext import commands as comms
from rich import logging as r_logging, traceback as r_traceback


def path(*filepath: t.Iterable[str]) -> str:
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


def _rich_logger(log_type: int = logging.INFO) -> logging.Logger:
    r_traceback.install()

    logging.basicConfig(
        level=log_type, format='%(message)s', datefmt="[%c]", handlers=[r_logging.RichHandler()]
    )

    return logging.getLogger("rich")


def _cleanup(folders: t.Union[list, str] = 'tmp') -> None:
    folders = [folders] if isinstance(folders, str) else folders

    for folder in folders:
        if os.path.isdir(path(folder)):
            for item in os.listdir(path(folder)):
                if ['.log', '.pycache', '.png'] in item[-4:]:
                    os.remove(path(folder, item))

        else:
            raise FileNotFoundError(f'Folder {folder} could not be located.')


class Bot(comms.Bot):

    def __init__(self, *args, **kwargs) -> None:
        self.log = kwargs.pop('log')

        super().__init__(*args, **kwargs)

        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)

        except IndexError as e:
            self.log.critical(
                f'{e}: Config file found, but token(s) could not be read properly.')

        except FileNotFoundError as e:
            self.log.critical(
                f'{e}: Config file not found. Please refer to the README when setting up.')

        self.add_cog(Development(self))

        asyncio.get_event_loop().run_until_complete(self.load_extensions())

    async def load_extensions(self, blocked_extensions: t.Union[str, list] = None) -> None:
        extensions = await self.get_extensions()
        broken_extensions = []

        for extension in extensions:
            try:
                self.load_extension(extension)

            except Exception as e:
                broken_extensions.append((extension, e))

        for extension, error in broken_extensions:
            raise comms.ExtensionError(f'{extension}: {error}')

    async def get_extensions(self) -> t.List[str]:
        extensions = []

        for folder in os.listdir(path('cogs')):
            extensions.extend(
                [f'cogs.{folder}.{i[:-3]}' for i in os.listdir(
                    path('cogs', folder)) if i[-3:] == '.py']
            )

        return extensions

    async def on_ready(self) -> None:
        self.log.warning('Awaiting...')

    async def logout(self) -> None:

        return await super().logout()


class Development(comms.Cog):

    def __init__(self, bot: comms.Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: comms.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    async def _reload(self, ctx: comms.Context) -> None:
        for cog in await self.bot.get_extensions():
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            except Exception as e:
                return self.bot.log.warning(f'Error while loading "{cog}" error: {e}')

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    async def _exit(self, ctx: comms.Context) -> None:
        self.bot.log.warning('logging out...')

        await ctx.bot.logout()


if __name__ == "__main__":
    if not os.path.isdir(path('tmp')):
        os.mkdir(path('tmp'))

    bot = Bot(
        command_prefix=';', case_insensitive=True, help_command=None, log=_rich_logger()
    )

    try:
        bot.run(bot.config['discord'], bot=True, reconnect=True)

    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        bot.log.critical('Improper token has been passed.')

    bot.log.warning('Cleaning up tmp/...')
    _cleanup()
    bot.log.info('Cleanup complete.')
