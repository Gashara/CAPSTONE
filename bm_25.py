import math
from collections import Counter, defaultdict

class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.N = len(corpus)
        self.avg_doc_len = sum(len(doc) for doc in corpus) / self.N
        self.doc_freqs = self._calculate_doc_freqs()
        self.idf = self._calculate_idf()

    def _calculate_doc_freqs(self):
        doc_freqs = defaultdict(int)
        for doc in self.corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                doc_freqs[term] += 1
        return doc_freqs

    def _calculate_idf(self):
        idf = {}
        for term, freq in self.doc_freqs.items():
            idf[term] = math.log(1 + (self.N - freq + 0.5) / (freq + 0.5))
        return idf

    def _calculate_tf(self, doc):
        tf = Counter(doc)
        return tf

    def score(self, query, doc):
        score = 0.0
        doc_len = len(doc)
        tf = self._calculate_tf(doc)
        for term in query:
            if term not in tf:
                continue
            term_freq = tf[term]
            idf = self.idf.get(term, 0)
            score += idf * (term_freq * (self.k1 + 1)) / (term_freq + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len)))
        return score

    def get_scores(self, query):
        scores = []
        for doc in self.corpus:
            scores.append(self.score(query, doc))
        return scores



