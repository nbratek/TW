from concurrent.futures import ThreadPoolExecutor


class Scheduler:
    def __init__(self, max_workers=8):
        self.tasks = []
        self.max_workers = max_workers

    def add_task(self, task, *args):
        self.tasks.append((task, args))

    def run(self, auto_clear=True):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(task[0], *task[1]) for task in self.tasks]
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error executing task: {e}")
                    results.append(None)
        if auto_clear:
            self.tasks = []
        return results


