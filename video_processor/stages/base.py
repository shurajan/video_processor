from abc import ABC, abstractmethod

class ProcessingStage(ABC):
    @abstractmethod
    def execute(self, video_info, context: dict) -> dict:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
