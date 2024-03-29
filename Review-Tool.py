# -*- coding: utf-8 -*-

import json, requests, sklearn.metrics, sklearn.model_selection, joblib, sklearn.tree, textblob, sklearn.neural_network, sklearn.neighbors
import warnings

warnings.filterwarnings('ignore')

response = requests.get('https://dgoldberg.sdsu.edu/515/appliance_reviews.json')

#Model Selecting Procecss
def model_selector(): 
    if ((dt_accuracy > knn_accuracy and dt_accuracy > nn_accuracy)): 
        print('Decision Tree model performed the best; saved to model.joblib.')
    elif ((knn_accuracy > dt_accuracy and knn_accuracy > nn_accuracy)):
        print('K-Nearest Neighbors model performed the best; saved to model.joblib.')
    elif ((nn_accuracy >= dt_accuracy and nn_accuracy > knn_accuracy)):
        print('Neural Network model performed the best; saved to model.joblib')

if response:
    data = response.json()
    x = []
    y = []
    
    for line in data:
        review = line['Review']
        stars = line['Stars']
        safety_hazard = line['Safety hazard']


        length = (len(review))

        # Sentiment Analysis
        blob = textblob.TextBlob(review)
        polarity = blob.polarity
        subjectivity = blob.subjectivity

        # Adding to empty lists
        inner_list = [length, stars, polarity, subjectivity]
        x.append(inner_list)
        y.append(safety_hazard)
    
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y)

    # Decision Tree
    dt_clf = sklearn.tree.DecisionTreeClassifier()
    dt_clf = dt_clf.fit(x_train, y_train)
    dt_predictions = dt_clf.predict(x_test)
    dt_accuracy = round(sklearn.metrics.accuracy_score(y_test, dt_predictions), 2)
    print("Decision Tree Accuracy:", dt_accuracy)


    # KNN
    knn_clf = sklearn.neighbors.KNeighborsClassifier(5)
    knn_clf = knn_clf.fit(x_train, y_train)
    knn_predictions = knn_clf.predict(x_test)
    knn_accuracy = round(sklearn.metrics.accuracy_score(y_test, knn_predictions), 2)
    print("K-Nearest Neighbors Accuracy:", knn_accuracy)


    # Neural Network
    nn_clf = sklearn.neural_network.MLPClassifier()
    nn_clf = nn_clf.fit(x_train, y_train)
    nn_predictions = nn_clf.predict(x_test)
    nn_accuracy = round(sklearn.metrics.accuracy_score(y_test, nn_predictions), 2)
    print("Neural Network Accuracy:", nn_accuracy)


    #Exporting models using joblib
    joblib.dump((dt_clf, knn_clf, nn_clf), 'model.joblib')

    #Model Selector
    model_selector()

else:
    print("Sorry, Connection Error.")
