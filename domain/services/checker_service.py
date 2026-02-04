from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase
from infrastructure.parsers.parser import ProductParser
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from application.use_cases.check_price import CheckPriceUseCase

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler



class CheckerService:
    def __init__(
        self,
        bot: Bot,
        uow_factory: UnitOfWorkFactory,
        parser: ProductParser
    ):
        self.bot = bot
        self.uow_factory = uow_factory
        self.parser = parser
        self.scheduler = AsyncIOScheduler()

    async def run_check(self) -> None:
        async with self.uow_factory() as uow:
            collector = Collector(uow)
            use_case = CheckPriceUseCase(uow)
            urls_for_parsing = await collector.collect_data_for_parsing()
        
            

            

