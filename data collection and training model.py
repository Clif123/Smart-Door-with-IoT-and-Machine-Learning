# compare algorithms
# Everything should load without error. If you have an error, stop. You need a working SciPy
# environment before continuing.
from pandas import read_csv
from matplotlib import pyplot
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pickle

# Load libraries
from sklearn.ensemble import AdaBoostClassifier
#from sklearn import datasets
# Import train_test_split function
#from sklearn.model_selection import train_test_split
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

#Load dataset
#If you do have network problems, you can download the iris.csv file into your working directory
#and load it using the same method, changing URL to the local file name.
#https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv

#url = "C:\Users\nicho\Downloads\velocity_fast_towards.csv"
names = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','class']
dataset = read_csv('Sus_data.csv', names=names)

#We can get a quick idea of how many instances (rows) and how many attributes (columns) the data
#contains with the shape property. You should see 150 instances and 5 attributes
#shape
print(dataset.shape)
#You should see the first 20 rows of the data:
# head
print(dataset.head(30))
#Now we can take a look at a summary of each attribute.
#This includes the count, mean, the min and max values as well as some percentiles.
#descriptions
#We can see that all of the numerical values have the same scale (centimeters)
#and similar ranges between 0 and 8 centimeters.
print(dataset.describe())
#Let’s now take a look at the number of instances (rows) that belong to each class.
#We can view this as an absolute count.
#We can see that each class has the same number of instances (50 or 33% of the dataset).
#class distribution
print(dataset.groupby('class').size())
#Given that the input variables are numeric, we can create box and whisker plots of each.
#This gives us a much clearer idea of the distribution of the input attributes
#box and whisker plots

# dataset.plot(kind='box', subplots=True, layout=(5,6), sharex=False, sharey=False)
# pyplot.show()


#We can also create a histogram of each input variable to get an idea of the distribution.
#It looks like perhaps two of the input variables have a Gaussian distribution.
#This is useful to note as we can use algorithms that can exploit this assumption.
#histograms

# dataset.hist()
# pyplot.show()
#First, let’s look at scatterplots of all pairs of attributes.
#This can be helpful to spot structured relationships between input variables.
#Note the diagonal grouping of some pairs of attributes.
#This suggests a high correlation and a predictable relationship.
#scatter plot matrix
# scatter_matrix(dataset)
# pyplot.show()
#We will split the loaded dataset into two, 80% of which we will use to train,
#evaluate and select among our models,
#and 20% that we will hold back as a validation dataset.
#You now have training data in the X_train and Y_train for preparing models and
#a X_validation and Y_validation sets that we can use later.
#Notice that we used a python slice to select the columns in the NumPy array.
#Split-out validation dataset
array = dataset.values
X = array[:,0:61] #preparing the question #till 31
y = array[:,61]  #preparing the answer #till 31
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1,
shuffle=True)
#Let’s test 3 different algorithms:
#K-Nearest Neighbors (KNN).
#Classification and Regression Trees (CART).
#Support Vector Machines (SVM).
#This is a good mixture of nonlinear (KNN, CART and SVM) algorithms.
# Check Algorithms
models = []
models.append(('KNN', KNeighborsClassifier()))
# models.append(('CART', DecisionTreeClassifier()))
# models.append(('SVM', SVC(gamma='auto')))
#We now have 3 models and accuracy estimations for each.
#We need to compare the models to each other and select the most accurate.
#Evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
# Make predictions on validation dataset
print("################Printing the results obtained from 'KNN'#####################")
model =  KNeighborsClassifier()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)
#We can evaluate the predictions by comparing them to the expected results
#in the validation set, then calculate classification accuracy,
#as well as a confusion matrix and a classification report.
#Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
#We can see that the accuracy is 0.966 or about 96% on the hold out dataset.
#The confusion matrix provides an indication of the three errors made.
#Finally, the classification report provides a breakdown of each class by precision,
#recall, f1-score and support showing excellent results
#(granted the validation dataset was small).

print("################Printing the results obtained from 'DecisionTree'#####################")
model = DecisionTreeClassifier()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)
#We can evaluate the predictions by comparing them to the expected results
#in the validation set, then calculate classification accuracy,
#as well as a confusion matrix and a classification report.
#Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


# print("#####################Printing the results obtained from 'SVM'#####################")
# model = SVC(gamma='auto')
# model.fit(X_train, Y_train)
# predictions = model.predict(X_validation)
# #We can evaluate the predictions by comparing them to the expected results
# #in the validation set, then calculate classification accuracy,
# #as well as a confusion matrix and a classification report.
# #Evaluate predictions
# print(accuracy_score(Y_validation, predictions))
# print(confusion_matrix(Y_validation, predictions))
# print(classification_report(Y_validation, predictions))


#Creating adaboost model
# svc = SVC(probability=True, kernel='rbf')
# abc = AdaBoostClassifier(n_estimators=50, base_estimator=svc,learning_rate=1)
# mod1 = abc.fit(X_train,Y_train)
# y_pred = mod1.predict(X_validation)

# print("ADABOOST")
# print("Accuracy:",metrics.accuracy_score(Y_validation, y_pred))
# print(classification_report(Y_validation, y_pred))



model = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth = 5), n_estimators=200, learning_rate = 1.35, random_state = 2)
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)
#We can evaluate the predictions by comparing them to the expected results
#in the validation set, then calculate classification accuracy,
#as well as a confusion matrix and a classification report.
#Evaluate predictions
print('##############################################################################')
print("ADABOOSTED Decision Tree")
print("Accuracy:",metrics.accuracy_score(Y_validation, predictions))
print(classification_report(Y_validation, predictions))











# with open("machine_modelsus.pickle", "wb") as file:
#     pickle.dump(model, file)
#     
# print ("Model saved.")
