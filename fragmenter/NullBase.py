from abc import ABC, abstractmethod


class NullBase(ABC):

    """
    Abstract class for generating null model parcellations.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self):

        pass
