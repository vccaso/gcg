class BaseAgent:
    def run(self, **kwargs):
        raise NotImplementedError("Subclasses must implement the run method")
