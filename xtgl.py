import math

W = dict()
train = {'A': {'a', 'b', 'd'}, 'B': {'a', 'c'}, 'C': {'b', 'e'}, 'D': {'c', 'd', 'e'}}  # {'a','b','c'}是一个集合
for u in train.keys():
    for v in train.keys():
        if u == v:
            continue

        W.update({u: {v: len(train[u] & train[v])}})  # 计算分子，'&'是 Python中集合的并运算
        W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)  # 分子/分母

for u, v_similarity in W.items():
    print(u, 'corresponds to', v_similarity)
