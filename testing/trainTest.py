import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

allText_dir = '/Users/summer-2024/Desktop/assignment_214232_export/allText'
data = []

# add each txt file to data
for filename in os.listdir(allText_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(allText_dir, filename)
        with open(file_path, 'r') as file:
            content = file.read()
            data.append(content)

# prep data
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

max_epochs = 10
vec_size = 150
alpha = 0.025

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                dm=1)

model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.epochs)
    model.alpha -= 0.0002
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")
