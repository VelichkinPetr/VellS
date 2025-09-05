
from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from buisness_logic.services.TestsDataService import TestsDataService

class TestDataServiceMiddleware(BaseMiddleware):

    def __init__(self, test_data_service: TestsDataService ):
        self.test_data_service = test_data_service

    async def __call__(self, handler: Callable, event: Message, data: Dict[str,Any]) -> Any:
        data['test_data_service'] = self.test_data_service
        return await handler(event, data)

class TestDataServiceMiddlewareCallback(BaseMiddleware):

    def __init__(self, test_data_service: TestsDataService):
        self.test_data_service = test_data_service

    async def __call__(self, handler: Callable, event: CallbackQuery, data: Dict[str, Any]) -> Any:
        data['test_data_service'] = self.test_data_service
        return await handler(event, data)