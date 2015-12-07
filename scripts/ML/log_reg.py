from sklearn import linear_model
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix

def split_comma(string):
    return map(float, str.split(string, ','))

def get_label(string):
    return int(string)

def main():
    Xfile = open('X.txt','r')
    Xfile.readline()
    X_original = map(split_comma, Xfile.read().splitlines())
    #print X
    y = map(get_label, open('y.txt', 'r').read().splitlines())
    #print y

    X = preprocessing.normalize(X_original)
    print len(X_original)
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

    log_reg = linear_model.LogisticRegression()
    log_reg.fit(X_train,y_train)
    
    train_accuracy = log_reg.score(X_train, y_train)
    test_accuracy = log_reg.score(X_test, y_test)
    print "Train accuracy = %f" % (train_accuracy)
    print "Test accuracy = %f" % (test_accuracy)

    print log_reg.coef_
    print log_reg.intercept_


#    print log_reg.predict(X_test)
    cm = confusion_matrix(y_test, log_reg.predict(X_test))
    print cm
    print 'Class\tPrecision\tRecall\t\tF1'
    P0 = float(cm[0][0])/(cm[0][0]+cm[1][0])
    R0 = float(cm[0][0])/(cm[0][0]+cm[0][1])
    F0 = 2*P0*R0/(P0+R0)
    P1 = float(cm[1][1])/(cm[1][1]+cm[0][1])
    R1 = float(cm[1][1])/(cm[1][1]+cm[1][0])
    F1 = 2*P1*R1/(P1+R1)
    print '0\t%f\t%f\t%f'%(P0,R0,F0)
    print '1\t%f\t%f\t%f'%(P1,R1,F1)
    
    
main()
