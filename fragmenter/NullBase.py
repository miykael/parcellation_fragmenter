from abc import ABC, abstractmethod


class NullBase(ABC):

    """
    Null model base class.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self):

        pass
