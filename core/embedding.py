import math
import re
from collections import Counter

class SimpleEmbedding:
    """
    Very simple local embedding:
    text -> word frequency vector
    (Explainable, no external model)
    """

    def embed(self, text: str):
        tokens = re.findall(r"\b\w+\b", text.lower())
        freq = Counter(tokens)
        return dict(freq)
