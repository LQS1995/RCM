def PersonalRank(G,alpha,root,max_step):

	rank = dict()#
	rank = {x: 0 for x in G.keys()}#初始化，将二分图中所有结点（包括所有的用户结点和物品结点）的访问概率（即PR，也可称为重要度）初始化为0
	rank[root] = 1 #为用户root进行推荐（即计算用户u对所有物品感兴趣的程度）

	for k in range(max_step):
		tmp = {x: 0 for x in G.keys()}
		for i, ri in G.items():
			for j, wij in ri.items():
				if j not in tmp: #保险起见，其实上边tmp在初始化时已经将所有的结点都包含进了
					tmp.update({j: 0})
				tmp[j] += alpha * rank[i] / (1.0 * len(ri))
				if j == root:
					tmp[j] += 1 - alpha
		rank = tmp
	return rank

G = {'A': {'a': 1, 'c': 1},
     'B': {'a': 1, 'b': 1, 'c': 1, 'd': 1},
     'C': {'c': 1, 'd': 1},
     'a': {'A': 1, 'B': 1},
     'b': {'B': 1},
     'c': {'A': 1, 'B': 1, 'C': 1},
     'd': {'B': 1, 'C': 1}} #节点和出边的尾节点，构成了二分图G； 边E(i,j)的权重wij设置为1。

alpha = 0.85
result = PersonalRank(G,alpha,'A',100)
print(result)
