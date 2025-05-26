from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        """Override this method in each task class"""
        pass

    def __call__(self):
        """Allow tasks to be executed like functions"""
        return self.run()
