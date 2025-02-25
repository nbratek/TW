from Scheduler import Scheduler
import numpy as np


class GaussianElimination:
    def __init__(self, matrix, n):
        self.matrix = matrix
        self.n = n
        self.m = np.empty((self.n, self.n))
        self.t = np.empty((self.n, self.n + 1, self.n))

    def task(fun):
        def wrapper(self, *args, **kwargs):
            print(f"Running task: {fun.__name__} with args {args}, {kwargs}")
            return fun
        return wrapper

    @task
    def task_A(self, i, k):
        self.m[i, k] = self.matrix[k, i] / self.matrix[i, i]

    @task
    def task_B(self, i, j, k):
        self.t[i, j, k] = self.matrix[i, j] * self.m[i, k]

    @task
    def task_C(self, i, j, k):
        self.matrix[k, j] -= self.t[i, j, k]

    def pivot(self, i):
        max_row = np.argmax(abs(self.matrix[i:, i])) + i
        if i != max_row:
            self.matrix[[i, max_row]] = self.matrix[[max_row, i]]
        if self.matrix[i, i] == 0:
            raise ValueError("Matrix is singular and cannot be solved")

    def resolve_backwards(self):
        for k in range(self.n - 1, 0, -1):
            if self.matrix[k, k] == 0:
                raise ValueError("Division by zero encountered in backward substitution")
            for i in range(k):
                self.reduce_row(k, i)
        return self.matrix

    def reduce_row(self, i, k):
        factor = self.matrix[k, i] / self.matrix[i, i]
        self.matrix[k, i:] -= factor * self.matrix[i, i:]
        return self.matrix

    def run(self):
        scheduler = Scheduler(self.n)
        for i in range(self.n):
            for k in range(i + 1, self.n):
                scheduler.add_task(self.reduce_row, i, k)
            scheduler.run()
        self.matrix /= self.matrix[np.arange(self.n), np.arange(self.n)][:, np.newaxis]
        self.matrix = self.resolve_backwards()
        return self.matrix

