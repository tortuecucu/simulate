from random import random, gauss
from src.model.tipsters import RatioTipster
from abc import ABC, abstractmethod

class BooleanTipster(RatioTipster, ABC):
    """Tipster that only returns a boolean value

    """
    @abstractmethod
    def _calculate(self)->bool:
        pass
    def forecast(self) -> bool:
        return super().forecast()

class LinearBooleanTipster(BooleanTipster):
    """Boolean Tipster with linear toss up. returns True for all values less or equal to success ratio

    """
    def __init__(self, success_ratio:float) -> None:
        assert success_ratio >=0 and success_ratio <= 1
        super().__init__()
        self._success_ratio=success_ratio
    def _calculate(self) -> bool:
        return random()<=self._success_ratio

class GaussianBooleanTipster(BooleanTipster):
    """Boolean Tipster with a gaussian distribution. returns True for all values less or equal to success ratio

    Args:
        BooleanTipster (_type_): _description_
    """
    def __init__(self, mu:float, sigma:float, success_ratio:float, retry:bool=True) -> None:
        assert success_ratio >=0 and success_ratio <= 1
        super().__init__()
        self.mu=mu
        self.sigma=sigma
        self.retry=retry
        self._success_ratio=success_ratio
    
    def _calculate(self) -> bool:
        attempts=0
        while result:=gauss(self.mu, self.sigma) < 0 or result > 0 and attempts < 1000 and self.retry:
            pass
        return result<=self._success_ratio