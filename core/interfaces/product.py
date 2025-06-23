from abc import ABC, abstractmethod

class IProductRepo(ABC):
    @abstractmethod
    def save():
        pass

    @abstractmethod
    def find_all():
        pass

    @abstractmethod
    def find_by_url():
        pass