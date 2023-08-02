from abc import ABC, abstractmethod


class DetectionsInterface(ABC):
    @abstractmethod
    def save_detection(self, id_telegram, date, url_image):
        pass

    @abstractmethod
    def get_detection(self, id):
        pass

    @abstractmethod
    def get_all_detections(self):
        pass

    @abstractmethod
    def get_max_id_detections(self):
        pass
