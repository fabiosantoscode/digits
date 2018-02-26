from mnist import MNIST
from sklearn.neural_network import MLPClassifier

mndata = MNIST('samples')

images, labels = mndata.load_training()

classifier = MLPClassifier(
    solver='lbfgs',
    alpha=1e-5,
    hidden_layer_sizes=(50,),
    random_state=1
)

print('training')
classifier.fit(images, labels)

import pickle

pickle.dump(classifier, open('network.pickle', 'wb'))

