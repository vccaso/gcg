from abc import ABC, abstractmethod

class AudioModelBase(ABC):
    @abstractmethod
    def text_to_speech(self, text: str, output_path: str, voice: str = "", factor: float = 1.0) -> str:
        pass

    @abstractmethod
    def speech_to_text(self, audio_path: str) -> str:
        pass
