from sklearn import linear_model
from sklearn import cross_validation
from sklearn import ensemble
from sklearn import preprocessing

def split_comma(string):
    return map(float, str.split(string, ','))

def get_label(string):
    return int(string)

def main():
    X_original = map(split_comma, open('X.txt', 'r').read().splitlines())
    #print X
    y = map(get_label, open('y.txt', 'r').read().splitlines())
    #print y

    X = preprocessing.normalize(X_original)

    #m = len(X)
    #partition_point = int(m * 0.7)
    #print "Partition point = %d" % (partition_point)
    #X_train = X[0:partition_point]
    #X_test = X[partition_point:m]
    #y_train = y[0:partition_point]
    #y_test = y[partition_point:m]

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)
    print len(X_train), len(X_test), len(y_train), len(y_test)

    ones = sum(y_test)
    baseline = float(max(ones, len(y_test) - ones)) / len(y_test)
    print "Baseline = %f" % (baseline)

    rand_for = ensemble.RandomForestClassifier(max_depth=10)
    rand_for.fit(X_train,y_train)

    train_accuracy = rand_for.score(X_train, y_train)
    test_accuracy = rand_for.score(X_test, y_test)
    print "Train accuracy = %f" % (train_accuracy)
    print "Test accuracy = %f" % (test_accuracy)

    print rand_for.feature_importances_
main()
