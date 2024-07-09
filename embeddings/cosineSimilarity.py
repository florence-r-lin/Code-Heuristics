import numpy as np

# code from "How to IMPLEMENT Cosine Similarity from in Python" by DataStax <-- Medium
###################
# edit as needed, later will be replaced by inputs generated from the requests.py script
A = np.array([1, 1, 1, 1, 0])
B = np.array([1, 1, 0, 0, 1])
###################


def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    cosine_similarity = dot_product / (norm_A * norm_B)
    return cosine_similarity

print(cosine_similarity(A, B))