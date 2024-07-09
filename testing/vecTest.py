from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

model= Doc2Vec.load("d2v.model")
#to find the vector of a document which is not in training data
test_data = word_tokenize("This example accepts an integer N and returns a list of integers from 0 to N-1, **each divided by 2** NOTE: this is floating-point division...!".lower())
v1 = model.infer_vector(test_data)
print("V1_infer", v1)

# # to find most similar doc using tags
# similar_doc = model.docvecs.most_similar('1')
# print(similar_doc)


# to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
print(model.docvecs['1'])