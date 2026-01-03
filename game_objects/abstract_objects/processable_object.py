from abc import abstractmethod, ABC


class ProcessableObject(ABC):
    _time: int | float = 0
    _interval: int | float = 0

    @abstractmethod
    def process(self, delta_time: int, **kwargs):
        raise NotImplemented()
