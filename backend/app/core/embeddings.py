import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from app.core.config import settings

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class FaissIndex:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = None
        self.ids = []
        self._load_or_init()

    def _load_or_init(self):
        os.makedirs(os.path.dirname(settings.faiss_index_path), exist_ok=True)
        if os.path.exists(settings.faiss_index_path):
            self.index = faiss.read_index(settings.faiss_index_path)
            idmap = settings.faiss_index_path + ".ids"
            if os.path.exists(idmap):
                with open(idmap) as f:
                    self.ids = [line.strip() for line in f]
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def add(self, id_str, vector):
        vec = np.array([vector]).astype("float32")
        self.index.add(vec)
        self.ids.append(id_str)
        self._persist()

    def search(self, vector, k=5):
        vec = np.array([vector]).astype("float32")
        D, I = self.index.search(vec, k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx == -1: continue
            results.append((self.ids[idx], float(dist)))
        return results

    def _persist(self):
        faiss.write_index(self.index, settings.faiss_index_path)
        with open(settings.faiss_index_path + ".ids", "w") as f:
            f.write("\n".join(self.ids))

_model = None
_index = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model

def get_index():
    global _index
    if _index is None:
        _index = FaissIndex(dim=384)
    return _index

def embed_and_store(id_str: str, text: str):
    model = get_model()
    vec = model.encode(text if text.strip() else " ")
    idx = get_index()
    idx.add(id_str, vec.tolist())
