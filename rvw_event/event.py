from abc import ABC, abstractmethod

class RVWEvent(ABC):
    def __init__(self, cmd):
        self.cmd = cmd
        super().__init__()

    @abstractmethod
    def execute(self, argumente = []):
        return None