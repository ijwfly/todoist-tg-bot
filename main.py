import asyncio
import os

from aiogram import Router, Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message

from todoist_api_python.api_async import TodoistAPIAsync


TODOIST_TOKEN = os.getenv('TODOIST_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID'))


todoist = TodoistAPIAsync(TODOIST_TOKEN)
router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    if message.from_user.id != TELEGRAM_ADMIN_ID:
        return
    await message.answer(f"Привет, <b>{message.from_user.full_name}!</b>")


@router.message()
async def task_handler(message: Message) -> None:
    if message.from_user.id != TELEGRAM_ADMIN_ID:
        return

    try:
        task_title, *task_description = message.text.split('\n')
        task_description = '\n'.join(task_description)

        await todoist.add_task(task_title, description=task_description)
        await message.answer('Добавил задачу')
    except Exception as e:
        await message.answer('Что-то пошло не так: {}'.format(e))
    except:
        await message.answer('Что-то пошло не так')


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(TELEGRAM_TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
