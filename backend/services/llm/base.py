from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt or instruction.

        Returns:
            Generated text response.
        """
        pass