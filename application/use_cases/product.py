from infrastructure.database.unit_of_work import UnitOfWorkFactory

from application.tools.adapter import LinkAdapter


class CreateProduct:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, url: str, user_id: int):
        pass
