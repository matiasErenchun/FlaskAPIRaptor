from abc import ABC, abstractmethod


class ValidationResultInterface(ABC):

    @abstractmethod
    def save_validation_result(self):
        pass

    @abstractmethod
    def get_all_validation_result(self):
        pass
    