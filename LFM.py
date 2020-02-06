# LFM p and q are determinied by stochastic_gradient_descent
import random as rd, math as mt, operator as op


def SplitData(data, M, k, seed):
    test = []
    train = []
    rd.seed(seed)
    for user, item in data:
        if rd.randint(0, M) == k:  # generate a uniform random number in [0,M]
            test.append([user, item])
        else:
            train.append([user, item])
    return train, test


def list2dic(listdata):
    dicdata = dict()
    for user, item in listdata:
        if user not in dicdata.keys():
            dicdata[user] = []
            dicdata[user].append(item)
        else:
            dicdata[user].append(item)
    return dicdata


def CreateItemsPool(train):
    items = dict()
    items_pool = []
    for u, i in train:
        if i not in items.keys():
            items[i] = 1;
        else:
            items[i] += 1;
    for item, pop in sorted(items.items(), key=op.itemgetter(1), reverse=True):
        items_pool.append(item)
    return items_pool;


def SelectNegativeSample(items_pool, trainu):
    ret = dict()
    for i in trainu:  # generate positive samples
        ret[i] = 1
    n = 0
    for i in items_pool:  # generate negative samples
        if i in ret:
            continue
        ret[i] = 0
        n += 1
        if n > len(trainu):
            break
    return ret


def InitLFM(train, F):
    p = dict()
    q = dict()
    for u, i in train:
        if u not in p.keys():
            p[u] = [rd.random() / mt.sqrt(F) for x in range(0, F)]
        if i not in q.keys():
            q[i] = [rd.random() / mt.sqrt(F) for x in range(0, F)]
    return p, q


# def RMSE(test, p, q):
#    error = 0
#    for u, i, rui in test.items():
#        error += pow( Predict(u, i, p, q) - rui, 2)
#    return error/len(test)

def LearningLFM(item_pool, train, F, n, alpha, ld):
    p, q = InitLFM(train, F)
    train = list2dic(train)
    for step in range(0, n):
        for u, i in train.items():
            samples = SelectNegativeSample(items_pool, train[u])
            for item, rui in samples.items():
                eui = rui - sum(p[u][f] * q[item][f] for f in range(0, F))
                for f in range(0, F):
                    p[u][f] += alpha * (q[item][f] * eui - ld * p[u][f])
                    q[item][f] += alpha * (p[u][f] * eui - ld * q[item][f])
        alpha *= 0.9
    return p, q


def TestLFM(train, p, q, N):
    Allrank = dict()
    rank = dict()
    for u in train.keys():
        rank.clear()
        for i in q.keys():
            if i not in train[u]:
                if i not in rank:
                    rank[i] = 0
                    for f in range(0, F):
                        rank[i] += p[u][f] * q[i][f]
        Allrank[u] = []
        for item, pop in sorted(rank.items(), key=op.itemgetter(1), reverse=True)[0:N]:
            Allrank[u].append(item)
    return Allrank


def Precision(allrank, test, N):
    hit = 0
    all = 0
    for user in test.keys():
        tu = test[user]
        if user in allrank.keys():
            for item in allrank[user]:
                if item in tu:
                    hit += 1
            all += N
    return hit / (all * 1.0)


'''
main function
'''
filestring = 'D:/dataset/ml-1m/ratings.csv'
f = open(filestring, 'r')
data = []
# k=0;
while 1:
    line = f.readline()  # read data
    # k+=1;
    if not line:
        break
    # if k>1000:
    #    break;
    line = line.split("::")[:2]
    line[0] = int(line[0])
    line[1] = int(line[1])
    data.append(line)
f.close()
M = 8
seed = 3
N = 10  # top-N
F = 100
alpha = 0.02
ld = 0.01
n = 100
# for k in range(M-1):
train, test = SplitData(data, M, 1, seed)  # generate train data and test data
items_pool = CreateItemsPool(train)  # sort by popularity
p, q = LearningLFM(items_pool, train, F, n, alpha, ld)
test = list2dic(test)
train = list2dic(train)
allrank = TestLFM(train, p, q, N)
pre = Precision(allrank, test, N)
print("precision is \n", pre)


