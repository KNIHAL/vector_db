import math
import re
from collections import Counter, defaultdict

class TFIDFEmbedding:
    def __init__(self):
        self.df = defaultdict(int)   # document frequency
        self.total_docs = 0

    def _tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def fit(self, texts):
        self.df.clear()
        self.total_docs = len(texts)

        for text in texts:
            tokens = set(self._tokenize(text))
            for t in tokens:
                self.df[t] += 1

    def embed(self, text):
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        vector = {}

        for word, freq in tf.items():
            idf = math.log((self.total_docs + 1) / (self.df.get(word, 0) + 1)) + 1
            vector[word] = freq * idf

        return vector
