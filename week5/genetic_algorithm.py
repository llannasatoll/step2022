import matplotlib.pyplot as plt
import copy
import random

class GeneticAlgorithm:
    """
    遺伝的アルゴリズムを扱うクラス。

    Parameters
    ----------
    initial_population : list of Chromosome
        最初の世代の個体群。
    max_generations : int
        アルゴリズムで実行する最大世代数。
    crossover_probability : float
        交叉確率（0.0～1.0）。
    mutation_probability : float
        変異確率（0.0～1.0）。
    elite_selection_rate : float
        エリート選択方式で選ばれる個体の割合（0.0～1.0）。
    log : Log(自作class)
        ログ用に結果を残しておくインスタンス変数。

    nelites : int
        エリート選択方式で選ばれる個体の数。
    best_chromosome : Chromosome
        現在の世代で最良の個体。
    """
    def __init__(
        self, 
        initial_population,
        max_generations,
        crossover_probability,
        mutation_probability,
        elite_selection_rate,
        log):

        self._population = initial_population
        self._max_generations = max_generations
        self._crossover_probability = crossover_probability
        self._mutation_probability = mutation_probability
        self.log = log

        self.nelites = int(len(self._population)*elite_selection_rate)
        self.best_chromosome = self._get_best_chromosome_from_population()

    
    def selection(self):
        """
        エリート選択方式とルーレット選択方式で、次世代に残す子個体を選択する。
        割合はelite_selection_rateで決められる。

        Returns
        -------
        次世代に残す個体群。
        """

        selected_chromosomes = []

        #エリート選択方式
        #世代の中で経路が短かった上位の個体
        selected_chromosomes.extend(sorted(self._population, key=lambda x: x.get_path_length(self.log.dist))[:self.nelites])
        
        #ルーレット選択方式
        #経路の長さに反比例する重みが設定された状態で、ランダムに抽出された個体。
        #(経路が短い方が重みが大きく、長い方が小さくする)
        weights = [1.0 / chromosome.get_path_length(self.log.dist) for chromosome in self._population]
        n = len(self._population) - self.nelites
        selected_chromosomes.extend(random.choices(self._population, weights=weights, k=n))

        return selected_chromosomes


    def crossover(self, new_population):
        """
        交叉確率に基づいて、交叉する親を選び、ランダムなペアで交叉させる。

        Returns
        -------
        交叉後の個体群。
        """

        #交叉する親個体群の選択
        crossovers_chromosomes = []
        for child in new_population:
            random_val = random.random()
            if random_val < self._crossover_probability:
                crossovers_chromosomes.append(child)
                new_population.remove(child)

        #シャッフルして前から2つずつを親として交叉させる
        #奇数の場合は、残り一つは交叉せずそのまま引き継がれる
        i = 1
        random.shuffle(crossovers_chromosomes)
        while i < len(crossovers_chromosomes):
            new_population.extend(crossovers_chromosomes[i-1].cyclic_crossover(crossovers_chromosomes[i]))
            i += 2

        return new_population


    def mutate(self, new_population):
        """
        変異確率に基づいて、突然変異を行う。

        Returns
        -------
        突然変異の処理を行なった後の個体群。
        """
        for i in range(len(new_population)):
            random_val = random.random()
            if random_val < self._mutation_probability:
                new_population[i].swap_mutation()


    def _to_next_generation(self):
        """
        次世代の個体を生成し、個体群を、生成した次世代の個体群で置換する。
        """

        new_population = []
        new_population = self.selection() #選択
        new_population = self.crossover(new_population) #交叉
        new_population = self.mutate(new_population) #突然変異

        _population = new_population


    def run_algorithm(self):
        """
        遺伝的アルゴリズムを実行し、実行結果の個体のインスタンスを取得する。

        Returns
        -------
        アルゴリズム実行結果の個体。世代数に達した時点で一番経路の短い個体が設定される。
        """

        for generation_idx in range(self._max_generations):
            
            #ログ用
            if not generation_idx % (self._max_generations//self.log.steps):
                self.log.save_path(generation_idx, self.best_chromosome.path, self.best_chromosome.get_path_length(self.log.dist))

            best = copy.copy(self.best_chromosome)

            self._to_next_generation() #世代交代
            self.best_chromosome = self._get_best_chromosome_from_population()

            #今までで一番良い個体は必ず次世代へ引き継ぐ
            if self.best_chromosome.get_path_length(self.log.dist) > best.get_path_length(self.log.dist):
                self._population.remove(self.best_chromosome)
                self._population.append(best)
                self.best_chromosome = best

        self.log.save_path(generation_idx+1, self.best_chromosome.path, self.best_chromosome.get_path_length(self.log.dist))

        return self.best_chromosome.path
    

    def _get_best_chromosome_from_population(self):
        """
        個体群のリストから、経路が一番短い個体を取得する。

        Returns
        -------
            リスト内の経路が一番短い個体。
        """

        best_chromosome = self._population[0]
        shotest = self._population[0].get_path_length(self.log.dist)

        for chromosome in self._population:
            tmp = chromosome.get_path_length(self.log.dist)
            if tmp < shotest:
                best_chromosome = chromosome
                shotest = tmp

        return best_chromosome


class Chromosome:
    """
    各個体（今回は経路）を扱うクラス。

    Parameters
    ----------
    path : list
        その個体の経路。
    """
    def __init__(self, path):
        self.path = path


    def cyclic_crossover(self, another_parent):
        """
        交叉（循環交叉）
        2つの染色体から、点の組と位置の組が等しいグループを探し、グループ同士を交換する。

        Parameters
        ----------
        another_parent : Chromosome
            自分と交叉する相手の個体。

        Returns
        -------
            2つの親から交叉して生まれた2つの子個体。
        """

        child1_path = copy.copy(self.path)
        child2_path = copy.copy(another_parent.path)

        idx = random.randrange(len(self.path))
        val_1st = self.path[idx]
        val_next = -1

        #循環して、最初のcityに戻ってきたら終了
        while val_next != val_1st:
            val_next = another_parent.path[idx]
            child1_path[idx] = val_next
            child2_path[idx] = self.path[idx]

            #親1から、val_nextがあるindexを探す
            for i in range(len(self.path)):
                if self.path[i] == val_next:
                    break
            idx = i

        child1 = Chromosome(child1_path)
        child2 = Chromosome(child2_path)
        return child1, child2


    def swap_mutation(self):
        """
        突然変異（交換）
        ランダムに選択した2区間について、遺伝子を区間ごと交換する。
        """
        idx0, idx1, idx2, idx3 = sorted(random.sample(range(len(self.path)), k=4))
        mutated_path = self.path[:idx0] + self.path[idx2:idx3] + self.path[idx1:idx2] + self.path[idx0:idx1] + self.path[idx3:]
        self.path = mutated_path
    

    def get_path_length(self, dist):
        """
        個体の経路を取得する。

        Parameters
        ----------
        dist : list
            各点の距離が格納してあるリスト。

        Returns
        -------
            個体の経路。
        """
        N = len(self.path)
        path_length = sum(dist[self.path[i]][self.path[(i+1)%N]] for i in range(N))

        return path_length


class Log():
    """
    ログを扱うクラス。
    今回は、各都市の座標や座標間の距離もメンバ変数にすることで、経路の長さを求めやすくしている。

    Parameters
    ----------
    cities : list
        各都市の座標。
    dist : list
        各都市の座標間の距離。
    steps : int
        ログを出力するstep数。
    printer : int(0, 1)
        0 -> 標準出力なし
        1 -> 標準出力あり
    mode : int(0~2)
        初期個体群の生成方法
        0 -> ランダムな経路
        1 -> greedy
        2 -> greedy + 2opt
    """
    def __init__(self, cities, dist, steps, printer=0, mode=0):
        self.cities = cities
        self.dist = dist
        self.steps = steps
        self.index = 0
        self.printer = printer
        self.mode = mode


    def save_path(self, generation_idx, path, path_length):
        """
        与えれた個体の情報を出力する。

        Parameters
        ----------
        generation_idx : int
            その個体の世代数。
        path : list
            その個体の経路。
        path_length : float
            その個体の経路の長さ。
        """
        if self.printer:
            print(f'世代数 : {generation_idx}\t最良個体 :{path_length}')

        N = len(path)
        x, y = [], []
        modename = ["random", "2opt", "greedy+2pot"]

        for i in range(N+1):
            x.append(self.cities[path[i%N]][0])
            y.append(self.cities[path[i%N]][1])
        
        plt.plot(x, y)
        plt.title(f"{generation_idx}th : len={path_length}")
        plt.savefig(f"graph/{modename[self.mode]}_{len(path)}_{self.index}.png")

        plt.clf()
        self.index += 1


