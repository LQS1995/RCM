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
