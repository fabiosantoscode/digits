from mnist import MNIST
from sklearn.neural_network import MLPClassifier

mndata = MNIST('samples')

images, labels = mndata.load_training()

classifier = MLPClassifier(
    solver='sgd',
    alpha=0.0001,
    verbose=True,
    hidden_layer_sizes=(70,),
    random_state=1
)

print('training')
classifier.fit(images, labels)

import pickle

pickle.dump(classifier, open('network.pickle', 'wb'))

