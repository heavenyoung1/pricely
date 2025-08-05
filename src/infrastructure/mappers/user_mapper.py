if TYPE_CHECKING:
    from src.domain.entities import 

class UserMapper:
    @staticmethod
    def to_orm(user: User)