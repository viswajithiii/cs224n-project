from sklearn import linear_model
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn import svm
from sklearn.metrics import confusion_matrix
import sys

def split_comma(string):
    return map(float, str.split(string, ','))

def get_label(string):
    return int(string)

def main():
    if len(sys.argv) > 1:
        Xfilename = sys.argv[1]
        Yfilename = sys.argv[2]
    else:
        Xfilename = 'X.txt'
        Yfilename = 'y.txt'
    Xfile = open(Xfilename,'r')
    Xfile.readline()
    X_original = map(split_comma, Xfile.read().splitlines())
    #print X
    y = map(get_label, open(Yfilename, 'r').read().splitlines())
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

    svc = svm.SVC(C=0.001,verbose=True)
    svc.fit(X_train,y_train)
    print 'Fitted model. Now running on data ...'
    
    train_accuracy = svc.score(X_train, y_train)
    test_accuracy = svc.score(X_test, y_test)
    print "Train accuracy = %f" % (train_accuracy)
    print "Test accuracy = %f" % (test_accuracy)

#    print svc.coef_
#    print svc.intercept_


#    print log_reg.predict(X_test)
    cm = confusion_matrix(y_test, svc.predict(X_test))
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
