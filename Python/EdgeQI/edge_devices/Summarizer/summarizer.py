class Summarizer:
    def __init__(self):
        self.previous_results = {}

    def summarize(self, task_name, result):
        """
        Summarize or filter task result.
        Only forward if significant change or new data.
        """
        previous = self.previous_results.get(task_name)
        if previous != result:
            self.previous_results[task_name] = result
            print(f"[Summarizer] Change detected in '{task_name}', forwarding result.")
            return result
        else:
            print(f"[Summarizer] No significant change in '{task_name}', skipping send.")
            return None
