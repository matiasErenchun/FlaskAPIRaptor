from abc import ABC, abstractmethod


class ValidationResultInterface(ABC):

    @abstractmethod
    def save_validation_result(self, id_validation, option, comment):
        pass

    @abstractmethod
    def get_all_validations_result(self, source):
        pass

    @abstractmethod
    def get_validation_result_by_id(self, id_validation):
        pass
