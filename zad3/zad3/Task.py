class Task:
    def __init__(self, task_name, i, j=None, k=None):
        self.task_name = task_name
        self.i = i
        self.j = j
        self.k = k
        self.idx_task_name = self.print_task_name()

    def print_task_name(self):
        if self.task_name == "A":
            return f"{self.task_name}_{self.i}{self.k}"
        elif self.task_name in ["B", "C"]:
            return f"{self.task_name}_{self.i}{self.j}{self.k}"

    def __repr__(self):
        return self.idx_task_name


