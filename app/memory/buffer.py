class MemoryBuffer:
    def __init__(self, k=5):
        self.k = k
        self.data = []

    def add(self, item: str):
        self.data.append(item)

    def get_context(self):
        return "\n".join(self.data[-self.k:])