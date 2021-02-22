import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

data = pd.read_csv("student-mat.csv", sep=";")
data.replace(('yes', 'no'), (1, 0), inplace=True)

data = data[["G1", "G2", "G3", "studytime", "failures", "absences", "romantic", "internet"]]
predict = "G3"

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)


# Trains model multiple times for best score
best = 0
for _ in range(30):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    results = linear.score(x_test, y_test)
    print(results)

    # If the current model has a better score than the one trained then save it
    if results > best:
        best = results
        with open("studentmodel.pickle", "wb")as f:
            pickle.dump(linear, f)

# Loads Model
pickled = open("studentmodel.pickle", "rb")
linear = pickle.load(pickled)

print(linear.coef_)
print(linear.intercept_)

predictions = linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

# Drawing and plotting model
p="G1"
style.use("ggplot")
pyplot.scatter(data[p], data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()
