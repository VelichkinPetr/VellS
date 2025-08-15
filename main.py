import asyncio

from models.bot import create
from handlers.start import start_router
from handlers.modification import modification_router


async def main():
    bot, dp = create()
    dp.include_routers(start_router, modification_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
