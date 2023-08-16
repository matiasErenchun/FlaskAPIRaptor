from abc import ABC, abstractmethod


class DetectionsInterface(ABC):
    @abstractmethod
    def save_detection(self, id_telegram, date, url_image, source, detection_class):
        pass

    @abstractmethod
    def get_detection(self, id):
        pass

    @abstractmethod
    def get_all_detections(self, source, filter_class):
        pass

    @abstractmethod
    def get_max_id_detections(self):
        pass
