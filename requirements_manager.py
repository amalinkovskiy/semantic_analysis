import math
import re
from collections import defaultdict, Counter

STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'to', 'for', 'of', 'and', 'or', 'in', 'on',
    'be', 'able', 'shall', 'should'
}

REDUNDANT_PATTERNS = [
    r'\bthe system shall\b',
    r'\bthe system should\b',
    r'\buser shall be able to\b',
]

class RequirementManager:
    """Manage requirements and their embeddings in a simple vector store."""

    def __init__(self):
        self.requirements = {}
        self.vectors = {}
        self.vocab = set()
        self.edges = defaultdict(list)

    # Pre-processing steps -------------------------------------------------
    def preprocess(self, text):
        text = text.lower()
        text = self._remove_redundant_phrases(text)
        tokens = self._tokenize(text)
        tokens = [self._lemmatize(t) for t in tokens]
        tokens = [t for t in tokens if t not in STOP_WORDS]
        tags = self._extract_tags(tokens)
        tokens = tags + tokens
        return tokens

    def _remove_redundant_phrases(self, text):
        for pattern in REDUNDANT_PATTERNS:
            text = re.sub(pattern, '', text)
        return text

    def _tokenize(self, text):
        return re.findall(r'[a-z0-9]+', text)

    def _lemmatize(self, token):
        if token.endswith('ies') and len(token) > 3:
            return token[:-3] + 'y'
        if token.endswith('es') and len(token) > 3:
            return token[:-2]
        if token.endswith('s') and len(token) > 3:
            return token[:-1]
        return token

    def _extract_tags(self, tokens):
        tags = []
        if 'security' in tokens:
            tags.append('SECURITY')
        if 'performance' in tokens:
            tags.append('PERFORMANCE')
        if 'usability' in tokens:
            tags.append('USABILITY')
        return tags

    # Vector operations ----------------------------------------------------
    def _build_vector(self, tokens):
        vec = Counter(tokens)
        self.vocab.update(vec.keys())
        return vec

    def _cosine_similarity(self, vec1, vec2):
        keys = set(vec1) | set(vec2)
        dot = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in keys)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    # Public API -----------------------------------------------------------
    def add_requirement(self, req_id, text):
        tokens = self.preprocess(text)
        vec = self._build_vector(tokens)
        self.requirements[req_id] = text
        self.vectors[req_id] = vec
        self._update_graph(req_id)

    def _update_graph(self, new_id, threshold=0.2):
        new_vec = self.vectors[new_id]
        for req_id, vec in self.vectors.items():
            if req_id == new_id:
                continue
            sim = self._cosine_similarity(new_vec, vec)
            if sim >= threshold:
                self.edges[new_id].append(req_id)
                self.edges[req_id].append(new_id)

    def find_related(self, text, top_n=5):
        tokens = self.preprocess(text)
        vec = self._build_vector(tokens)
        sims = []
        for req_id, other_vec in self.vectors.items():
            sim = self._cosine_similarity(vec, other_vec)
            sims.append((sim, req_id))
        sims.sort(reverse=True)
        return [req for sim, req in sims[:top_n] if sim > 0]

    def integrate_new_requirement(self, req_id, text):
        related = self.find_related(text)
        self.add_requirement(req_id, text)
        return related
