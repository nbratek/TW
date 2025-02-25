class Dependency:
    def __init__(self, alphabet, transactions):
        self.alphabet = alphabet
        self.transactions = transactions
        self.dependency_relations = self.find_dependencies()
        self.independency_relations = self.find_independencies()

    def find_dependencies(self):
        dependencies = set()
        for symbol1 in self.alphabet:
            for symbol2 in self.alphabet:
                if symbol1 == symbol2:
                    dependencies.add((symbol1, symbol2))
                else:
                    if self._has_dependency(symbol1, symbol2):
                        dependencies.add((symbol1, symbol2))
                        dependencies.add((symbol2, symbol1))
        return dependencies

    def find_independencies(self):
        independencies = set()
        for symbol1 in self.alphabet:
            for symbol2 in self.alphabet:
                if (symbol1, symbol2) not in self.dependency_relations and (
                symbol2, symbol1) not in self.dependency_relations:
                    independencies.add((symbol1, symbol2))
        return independencies

    def _has_dependency(self, first, second):
        first_left, first_right = self._decompose_transaction(self.transactions.get(first))
        second_left, second_right = self._decompose_transaction(self.transactions.get(second))

        return (first_left in second_right) or (second_left in first_right)

    @staticmethod
    def _decompose_transaction(transaction):
        equal_index = transaction.find('=')
        if equal_index == -1:
            return "", ""
        left = transaction[:equal_index]
        right = transaction[equal_index + 1:]
        return left, right





