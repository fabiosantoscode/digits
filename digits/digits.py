import _pickle as pickle
from mnist import MNIST

mndata = MNIST('samples')

images, labels = mndata.load_training()
images_test, labels_test = mndata.load_testing()

try:
    classifier = pickle.load(open('network.pickle', 'rb'))
except IOError:
    print('You should run network.py to create the classifier')
    exit()

correct, wrong = 0, 0
for image, label in zip(images_test[-30:], labels_test[-30:]):
    [prediction] = classifier.predict([image])
    is_correct = prediction == label

    print(mndata.display(image), '=>', label)

    if is_correct:
        correct += 1
    else:
        wrong += 1

    print('correct' if is_correct else ('WRONG'), prediction)

print('score', (correct / (correct + wrong)) * 100, '%')
print('correct', correct, 'wrong', wrong)

