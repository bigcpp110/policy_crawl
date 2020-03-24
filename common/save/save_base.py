import abc


class SaveBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self,data):
        pass


