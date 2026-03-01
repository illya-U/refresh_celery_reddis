from abc import ABC, abstractmethod
from time import sleep


class AbstractPaymentProvider(ABC):
    @abstractmethod
    def pay(self, amount) -> bool:
        raise NotImplementedError("Subclasses must implement this method")


class StripePaymentProvider(AbstractPaymentProvider):
    def pay(self, amount) -> bool:
        sleep(10)
        print(f"Paying {amount} using Stripe")
        return True


class FakeProvider(AbstractPaymentProvider):
    def pay(self, amount) -> bool:
        sleep(5)
        print(f"Paying {amount} using fake provider")
        return False