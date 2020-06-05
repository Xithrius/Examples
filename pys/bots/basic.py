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
    """Returns absolute path from main caller file to another location.

    Args:
        filepath (:obj:`t.Iterable`): Arguments to add to the current filepath.

    Returns:
        str: filepath with OS based seperator.

    Examples:
        >>> print(path('tmp', 'image.png'))
        C:\\Users\\Xithr\\Documents\\Repositories\\Xythrion\\tmp\\image.png

    """
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


def _rich_logger(log_type: int = logging.INFO) -> logging.Logger:
    """Logs information with the rich library with fancy tracebacks.

    Args:
        log_type (:obj:`t.Union[str, int]`, optional): The level of logging to be used.
            Defaults to None.
        store_file (bool, optional): If the logs want to be stored.

    Returns:
        :obj:`logging.Logger`: The object that the bot will use to log information to.

    Raises:
        IndexError: If `log_type` isn't within log_types.

    """
    r_traceback.install()

    logging.basicConfig(
        level=log_type, format='%(message)s', datefmt="[%c]", handlers=[r_logging.RichHandler()]
    )

    # different message types: info, debug, warning, critical
    return logging.getLogger("rich")


def _cleanup(folders: t.Union[list, str] = 'tmp') -> None:
    """Cleans up folders after the running of the bot's blocking stops.

    Function will continue clearing files until it is done or a folder cannot be found.

    NOTE: THIS FUNCTION WILL DESTROY ALL FILES CONTAINING '.log', '.pycache', AND/OR '.png'.
          USE THIS FUNCTION WITH CARE.

    Args:
        folders (:obj:`t.Union[list, str]`, optional): Folder to have their contents cleared out.

    Returns:
        bool: Always None.

    Raises:
        FileNotFoundError: If one of the specified folders cannot be found.

    """
    folders = [folders] if isinstance(folders, str) else folders

    for folder in folders:
        if os.path.isdir(path(folder)):
            for item in os.listdir(path(folder)):
                if ['.log', '.pycache', '.png'] in item[-4:]:
                    os.remove(path(folder, item))

        else:
            raise FileNotFoundError(f'Folder {folder} could not be located.')


class Bot(comms.Bot):
    """A subclass where very important tasks and connections are created.

    Attributes:
        config (dict): Tokens and other items from `./config/config.json`.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of tasks and connections.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: Always None.

        """
        # Setting the logger before inheritence occurs.
        self.log = kwargs.pop('log')

        # Initializing the base class `Comms.bot` and inheriting all it's attributes and functions.
        super().__init__(*args, **kwargs)

        # Attempting to open config config
        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)

        # If the file could be found but not indexed properly.
        except IndexError as e:
            self.log.critical(
                f'{e}: Config file found, but token(s) could not be read properly.')

        # If the file could not be found.
        except FileNotFoundError as e:
            self.log.critical(
                f'{e}: Config file not found. Please refer to the README when setting up.')

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Loading the cogs in, one by one.
        asyncio.get_event_loop().run_until_complete(self.load_extensions())

    async def load_extensions(self, blocked_extensions: t.Union[str, list] = None) -> None:
        """Loading in the extensions for the bot.

        Args:
            blocked_extensions (:obj:`t.Union[str, list]`, optional): Extension(s) to not be loaded.

        Returns:
            bool: Always None.

        Raises:
            :obj:`ExtensionNotFound`: The extension could not be imported.
            :obj:`NoEntryPointError`: The extension does not have a setup function.
            :obj:`ExtensionFailed`: The extension or its setup function had an execution error.

        """
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
        """Acquiring extensions for the bot to load in.

        Returns:
            :obj:`t.List[str]`: A list containing cogs.

        Raises:
            FileNotFoundError: When the folder 'cogs' cannot be found.

        """
        extensions = []

        for folder in os.listdir(path('cogs')):
            extensions.extend(
                [f'cogs.{folder}.{i[:-3]}' for i in os.listdir(
                    path('cogs', folder)) if i[-3:] == '.py']
            )

        return extensions

    async def on_ready(self) -> None:
        """Updates the bot status when logged in successfully.

        Returns:
            bool: Always None.

        Raises:
           :obj:`discord.InvalidArgument`: If the activity type is invalid.

        """
        # await self.change_presence(
        #     activity=discord.Activity(
        #         type=discord.ActivityType.watching, name="graphs")
        # )

        self.log.warning('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure anything running is stopped properly.

        Returns:
            bool: Always None.

        """
        # Do extra stuff

        return await super().logout()


class Development(comms.Cog):
    """Cog required for development and control, along with the help command.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        Returns:
            bool: Always None.

        """
        self.bot = bot

    async def cog_check(self, ctx: comms.Context) -> bool:
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    async def _reload(self, ctx: comms.Context) -> None:
        """Gets the cogs within folders and loads them into the bot after unloading current cogs.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Raises:
            Anything besides comms.ExtensionNotLoaded when loading cogs.

        Command examples:
            >>> [prefix]r
            >>> [prefix]refresh

        """
        for cog in await self.bot.get_extensions():
            # Attempting to unload the load the extension back in.
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            # If the extension was created after the bot initialized startup.
            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            # If a fatal error occurs.
            except Exception as e:
                return self.bot.log.warning(f'Error while loading "{cog}" error: {e}')

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    async def _exit(self, ctx: comms.Context) -> None:
        """Makes the bot logout.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]exit

        """
        self.bot.log.warning('logging out...')

        await ctx.bot.logout()

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: comms.Context) -> None:
        """Giving help to a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None

        Command example(s):
            >>> [prefix]help

        """
        pass


if __name__ == "__main__":
    # Creating the `tmp` directory if it doesn't exist
    if not os.path.isdir(path('tmp')):
        os.mkdir(path('tmp'))

    # Initializing the subclass of `comms.Bot`.
    bot = Bot(
        command_prefix=';', case_insensitive=True, help_command=None, log=_rich_logger()
    )

    # Attempting to run the bot (blocking, obviously).
    try:
        bot.run(bot.config['discord'], bot=True, reconnect=True)

    # If the token is incorrect or not given.
    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        bot.log.critical('Improper token has been passed.')

    # Removing any stray files within the `tmp` directory
    bot.log.warning('Cleaning up tmp/...')

    _cleanup()

    bot.log.info('Cleanup complete.')
