from sentence_transformers import SentenceTransformer, util

# Load the sentence-transformer model for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')  # A popular lightweight model for semantic similarity


# Load the zero-shot classification model for NLI tasks (contradiction detection)

def get_text_similarity(embedding1, embedding2):
    # Compute cosine similarity
    similarity = util.cos_sim(embedding1, embedding2)
    return similarity.item()


def is_synonym(similarity, threshold=0.5):
    """
    Determine if two texts are synonyms based on a similarity threshold.
    """
    return similarity >= threshold


def similarity_tester(embedding1, embedding2):
    a = get_text_similarity(embedding1, embedding2)
    return [a, is_synonym(a)]
