class Metric():

    def __init__(self, train, test, GetRecommendation):
        '''
        :params: train, 训练数据
        :params: test, 测试数据
        :params: GetRecommendation, 为某个用户获取推荐物品的接口函数
        '''
        self.train = train
        self.test = test
        self.GetRecommendation = GetRecommendation
        self.recs = self.getRec()

    # 为test中的每个用户进行推荐
    def getRec(self):
        recs = {}
        for user in self.test:
            rank = self.GetRecommendation(user)
            recs[user] = rank
        return recs

    # 定义精确率指标计算方式
    def precision(self):
        all, hit = 0, 0
        for user in self.test:
            test_items = set(self.test[user])
            rank = self.recs[user]
            for item, score in rank:
                if item in test_items:
                    hit += 1
            all += len(rank)
        return round(hit / all * 100, 2)

    # 定义召回率指标计算方式
    def recall(self):
        all, hit = 0, 0
        for user in self.test:
            test_items = set(self.test[user])
            rank = self.recs[user]
            for item, score in rank:
                if item in test_items:
                    hit += 1
            all += len(test_items)
        return round(hit / all * 100, 2)

    # 定义覆盖率指标计算方式
    def coverage(self):
        all_item, recom_item = set(), set()
        for user in self.train:
            for item in self.train[user]:
                all_item.add(item)
        for user in self.test:
            rank = self.recs[user]
            for item, score in rank:
                recom_item.add(item)
        return round(len(recom_item) / len(all_item) * 100, 2)

    # 定义多样性指标计算方式
    def diversity(self):
        # 计算item_vec，每个tag的个数
        item_tags = {}
        for user in self.train:
            for item in self.train[user]:
                if item not in item_tags:
                    item_tags[item] = {}
                for tag in self.train[user][item]:
                    if tag not in item_tags[item]:
                        item_tags[item][tag] = 0
                    item_tags[item][tag] += 1

        # 计算两个item的相似度
        def CosineSim(u, v):
            ret = 0
            for tag in item_tags[u]:
                if tag in item_tags[v]:
                    ret += item_tags[u][tag] * item_tags[v][tag]
            nu, nv = 0, 0
            for tag in item_tags[u]:
                nu += item_tags[u][tag] ** 2
                for tag in item_tags[v]:
                    nv += item_tags[v][tag] ** 2
                return ret / math.sqrt(nu * nv)

                # 计算Diversity
            div = []
            for user in self.test:
                rank = self.recs[user]
                sim, cnt = 0, 0
                for u, _ in rank:
                    for v, _ in rank:
                        if u == v:
                            continue
                        sim += CosineSim(u, v)
                        cnt += 1
                sim = sim / cnt if sim != 0 else 0
                div.append(1 - sim)
            return sum(div) / len(div)

            # 定义新颖度指标计算方式

        def popularity(self):
            # 计算物品的流行度，为给这个物品打过标签的用户数
            item_pop = {}
            for user in self.train:
                for item in self.train[user]:
                    if item not in item_pop:
                        item_pop[item] = 0
                    item_pop[item] += 1

            num, pop = 0, 0
            for user in self.test:
                rank = self.recs[user]
                for item, score in rank:
                    # 取对数，防止因长尾问题带来的被流行物品所主导
                    pop += math.log(1 + item_pop[item]
                    num += 1
                    return round(pop / num, 6)

        def eval(self):
            metric = {'Precision': self.precision(),
                    'Recall': self.recall(),
                      'Coverage': self.coverage(),
                      'Diversity': self.diversity(),
                      'Popularity': self.popularity()}
            print('Metric:', metric)
            return metric