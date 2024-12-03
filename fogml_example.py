from sklearn import datasets, tree

from fogml.generators import GeneratorFactory

iris = datasets.load_iris()
X = iris.data
y = iris.target

clf = tree.DecisionTreeClassifier(random_state=3456)
clf.fit(X, y)
print( 'accuracy: ',clf.score(X,y))

factory = GeneratorFactory()
generator = factory.get_generator(clf)
generator.generate()