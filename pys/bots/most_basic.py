import json
import os
import typing as t
import sys

from discord.ext import commands as comms


def path(*filepath: t.Iterable[str]) -> str:
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


class Bot(comms.Bot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)

        except IndexError as e:
            print(f'{e}: Config file found, but token(s) could not be read properly.')

        except FileNotFoundError as e:
            print(f'{e}: Config file not found. Please refer to the README when setting up.')

        self.add_cog(Development(self))

    async def on_ready(self) -> None:
        print('Awaiting...')


class Development(comms.Cog):

    def __init__(self, bot: comms.Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: comms.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    async def _exit(self, ctx: comms.Context) -> None:
        print('logging out...')

        await ctx.bot.logout()


if __name__ == "__main__":
    bot = Bot(command_prefix=';', case_insensitive=True, help_command=None)

    bot.run(bot.config['discord'], bot=True, reconnect=True)
