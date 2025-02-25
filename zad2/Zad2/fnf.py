class Foata:
    def __init__(self, alphabet, word, dependency_rel):
        self.alphabet = sorted(alphabet)
        self.word = word
        self.dependence = self._prepare_dependencies_from_dependency_object(dependency_rel)

    def _prepare_dependencies_from_dependency_object(self, dependency_rel):
        return dependency_rel.dependency_relations

    def _initialize_stacks(self):
        stacks = {symbol: [] for symbol in self.alphabet}
        for symbol1 in reversed(self.word):
            for symbol2 in self.alphabet:
                if (symbol1, symbol2) in self.dependence:
                    if symbol1 != symbol2:
                        stacks[symbol2].append('*')
                    else:
                        stacks[symbol1].append(symbol1)
        return stacks

    def _process_stacks(self, stacks):
        fnf = []
        while stacks:
            current_block = self._get_top_elements(stacks)
            self._clean_stacks(stacks, current_block)
            if current_block:
                fnf.append(sorted(current_block))
            else:
                break
        return fnf

    def _get_top_elements(self, stacks):
        current_block = []
        for symbol in self.alphabet:
            stack = stacks[symbol]
            if stack and stack[-1] != '*':
                if stack[-1] not in current_block:
                    current_block.append(stack[-1])
        return current_block

    def _clean_stacks(self, stacks, current_block):
        for element in current_block:
            for symbol in self.alphabet:
                if (element, symbol) in self.dependence:
                    stacks[symbol].pop()

    def compute_Foata_Normal_Form(self):
        stacks = self._initialize_stacks()
        return self._process_stacks(stacks)

    @staticmethod
    def is_symbol_pair_dependent(dependency_set, symbol1, symbol2):
        return any(pair for pair in dependency_set if pair == (symbol1, symbol2))

    def fnf_to_string(self, fnf):
        return ''.join(f"({''.join(group)})" for group in fnf)
