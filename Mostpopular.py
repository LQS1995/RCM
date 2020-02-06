def MostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''

    items = {}
    for user in train:
        for item in train[user]:
            if item not in items:
                items[item] = 0
            items[item] += 1
    items = list(sorted(items.items(), key=lambda x: x[1], reverse=True))

    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        recs = [x for x in items if x[0] not in seen_items][:N]
        return recs

    return GetRecommendation