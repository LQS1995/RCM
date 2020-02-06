import math
train = dict();

train = {'A':{'a':1,'b':1,'d':1},
		 'B':{'a':1,'c':1},
		 'C':{'b':1,'e':1},
		 'D':{'c':1,'d':1,'e':1}
		}#此处物品a、b、c、d、e后面对应的值1，是用户对物品感兴趣的程度。比如'A':{'a':1}，是用户A对物品a感兴趣的程度。
		 #按理说感兴趣的程度应该是不同的数值，但此处，因为使用的是单一行为的隐反馈数据，所以所有的都定为1了。这里的感兴趣程度即书中p47页公式（用于计算用户u对物品i的感兴趣程度）中的rvi，可参考其介绍。

#1、build inverse table for item_users：通过用户-物品列表，建立物品-用户倒排表
item_users = dict()#存储物品-用户倒排表
for u,items in train.items():
	#print(u,'corresponds to',items)
	for i in items.keys():#遍历每一个用户的物品列表。
		#print(i)
		if i not in item_users:
			item_users[i] = set()
		item_users[i].add(u)#物品列表中的物品i，有用户u访问过

print('输出item_users[]')
for u,items in item_users.items():
	print(u,'corresponds to',items)
print('')

# 2、calculate co-rated items between users ：计算两个用户共同访问过的物品数，建立用户相似度矩阵C，C[u][v]=x，即表示u,v共同访问过的物品有x个。
C = dict()  # C[][]是一个嵌套的二维字典，eg：C = {'A':{'C':1,'B':1,'D':1}}
N = dict()  # N[]统计用户有过行为的物品数，最终N[A]=3,N[B]=2,N[C]=2,N[D]=3
for i, users in item_users.items():
    print(i, 'corresponds to ', users)  # 示例：('a', 'corresponds to ', set(['A', 'B']))

    for u in users:  # u遍历一遍物品i的users列表
        print(u, 'u in users')
        if u not in N.keys():
            N[u] = 0
        N[u] += 1  # 统计用户u有过行为的物品数

        for v in users:  # v遍历一遍物品i的users列表
            print(v, 'v in uers')
            if u == v:
                continue

            # 注意：二维“字典”新添一个key-value对时，需要判断key是否已经存在了
            if u not in C.keys():
                C.update({u: {v: 0}})

            if v not in C[u].keys():
                C[u].update({v: 0})

            C[u][v] += 1  # 用户u、v对同一个物品有过行为。经过u,v两层遍历，C[][]会成为一个对称矩阵。
            print(C)

print('\n输出N[]：')
for user, value in N.items():
    print(user, 'corresponds to', value)

print('\n输出C[][]：')
for u, related_users in C.items():
    print(u, 'corresponds to', related_users)

# 3、calculate final similarity matrix W ：计算最终相似度矩阵W
W = dict()
# 下面的两层迭代其实即C[u][v]=cuv。
for u, related_users in C.items():  # u为一级坐标
    for v, cuv in related_users.items():  # v为二级坐标，cuv即C[u][v]的值，即|N(u)∩N(v)|
        if u not in W.keys():
            W.update({u: {v: cuv / math.sqrt(N[u] * N[v])}})
        else:
            W[u].update({v: cuv / math.sqrt(N[u] * N[v])})

        print(W)

for u, related_users in W.items():
    print(u, 'corresponds to ', related_users)

#4 计算用户A对，自己没有过行为的物品，的感兴趣程度
def itemgetter(elem):
    return elem[1]

# 给用户A进行推荐，user = 'A'
user = 'A'
K = 3
rank = dict()
interacted_items = train[user]
for v, wuv in sorted(W[user].items(), key=itemgetter, reverse=True)[0:K]:
    for i, rvi in train[v].items():
        if i in interacted_items:
        	#即如果物品i，在用户user（此处为A）的，有过行为的列表中，（换句话说，用户user对物品i有过行为），将物品i过滤掉，不计算感兴趣程度。
        	continue;
else:
        	if i not in rank.keys():
        		rank.update({i:0})
        	rank[i] += wuv*rvi

# 得到结果rank
print('输出rank[]:')
print(rank)
