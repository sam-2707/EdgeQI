# EdgeQI/Core/summarizer/summarizer.py

class Summarizer:
    """
    Summarizes the results of tasks.
    """
    def __init__(self):
        pass

    def summarize(self, task_name, result):
        """
        Summarizes the result of a task.

        Args:
            task_name (str): The name of the task.
            result: The result of the task.

        Returns:
            str: The summarized result.
        """
        return f"Task '{task_name}' completed with result: {result}"
