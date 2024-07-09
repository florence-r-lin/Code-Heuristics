from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize


# prepping data, need to tokenize
data = [
    "lc_mult(N): Accepts an integer N and returns a list of integers from 0 to N-1, where each integer is multiplied by 2.",
    "lc_idiv(N): Accepts an integer N and returns a list of integers from 0 to N-1, where each integer is divided by 2 using integer division, truncating any remainder.",
    "lc_fdiv(N): Accepts an integer N and returns a list of integers from 0 to N-1, where each integer is divided by 2 using floating-point division, resulting in a float.",
    "unitfracs(N): Accepts an integer N and returns a list of N evenly spaced fractions within the unit interval [0, 1), where each fraction is x/N.",
    "scaledfracs(low, high, N): Accepts three parameters (low, high, N) and returns a list of N left endpoints uniformly distributed through the interval [low, high), scaled according to the range (high - low).",
    "sqfracs(low, high, N): Accepts three parameters (low, high, N) and returns the squares of each value obtained from the scaledfracs(low, high, N) function, producing a list of squared endpoints.",
    "f_of_fracs(f, low, high, N): Accepts a function f and three parameters (low, high, N), applies function f to each value obtained from the scaledfracs(low, high, N) function, and returns a list of the results.",
    "integrate(f, low, high, N): Accepts a function f and three parameters (low, high, N), and estimates the definite integral of function f over the interval [low, high] by summing the areas of rectangles under f, using N uniform steps.",
    "c(x): Accepts a value x and returns the y-coordinate of a semicircle with radius two centered at the origin, calculated as the positive square root of (4 - x^2)."
]

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

max_epochs = 42
vec_size = 20
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
