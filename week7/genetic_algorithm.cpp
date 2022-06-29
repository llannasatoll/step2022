#include <iostream>
#include <vector>
#include <random>
#include "genetic_algorithm.h"

using namespace std;


/**
 * @brief Chromosomeクラスの初期化メソッド
 * 
 * @param path 経路
 * @param dist 各都市間の距離のリスト
 */
void Chromosome::init(vector<int> path, vector<vector<double> > dist){
    this->path = path;
    this->get_path_length(dist);
}


/**
 * @brief 循環交叉
 * 
 * @param another_parent 交叉する相手の個体
 * @param dist 各都市間の距離のリスト
 * @return vector<int> 交叉して生まれた個体
 */
vector<int> Chromosome::cyclic_crossover(vector<int> another_parent, vector<vector<double> > dist){
    int i, idx, N = this->path.size();
    double longest = -1.0;

    // 賢い交叉
    // 循環交叉するときに、一番距離の長い辺を構成する点から循環交叉を始めることで、より良い個体が生まれることを期待する。
    for(i=0; i<N; i++)
        if(dist[this->path[i]][this->path[(i+1)%N]] > longest){
            idx = i;
            longest = dist[this->path[i]][this->path[(i+1)%N]];
        } 
    int val_1st = this->path[idx];
    int val_next = -1;

    vector<int> child1_path = this->path;

    while(val_next != val_1st){
        val_next = another_parent[idx];
        child1_path[idx] = val_next;
        for(i=0; i<this->path.size(); i++)
            if(this->path[i] == val_next) break;
        idx = i;
    }
    return child1_path;
}


/**
 * @brief 突然変異
 * 
 */
void Chromosome::swap_mutation(){
    // 突然変異で生まれた個体が
    random_device get_rand_dev;
    mt19937 get_rand_mt(get_rand_dev());
    shuffle(this->path.begin(), this->path.end(), get_rand_mt);
    
    int i;
    vector<int> randlist(4), tmp;
    for(i = 0; i < 4; i++) randlist[i] = rand()%this->path.size();
    sort(randlist.begin(), randlist.end());

    for(int j = 0; j < randlist[0]; j++) tmp.push_back(this->path[j]);
    for(int j = randlist[2]; j < randlist[3]; j++) tmp.push_back(this->path[j]);
    for(int j = randlist[1]; j < randlist[2]; j++) tmp.push_back(this->path[j]);
    for(int j = randlist[0]; j < randlist[1]; j++) tmp.push_back(this->path[j]);    for(int j = randlist[1]; j < randlist[2]; j++) tmp.push_back(this->path[j]);
    for(int j = randlist[3]; j < this->path.size(); j++) tmp.push_back(this->path[j]);

}


/**
 * @brief 個体の経路から、総距離を計算する
 * 
 * @param dist 各都市間の距離のリスト
 */
void Chromosome::get_path_length(vector<vector<double> > dist){
    int N = this->path.size();
    vector<float> each_path_length;

    for(int i=0; i<N; i++) each_path_length.push_back(dist[this->path[i]][this->path[(i+1)%N]]); // pathから、各辺の長さを求める
    this->length = accumulate(each_path_length.begin(), each_path_length.end(), 0); // その合計値をメンバ変数lengthに格納
}


/**
 * @brief GeneticAlgorithmクラスの初期化メソッド
 * 
 * @param _population 世代の個体群
 * @param _max_generations 最大世代数（厳密には＋1）
 * @param _crossover_probability 交叉確率（0~1）
 * @param _mutation_probability 変異確率（0~1）
 * @param _elite_selection_rate エリート選択方式で選ばれる個体の割合
 * @param _dist 各都市間の距離の座標
 */
void GeneticAlgorithm::init(vector<Chromosome> _population,
                            int _max_generations, 
                            float _crossover_probability, 
                            float _mutation_probability, 
                            float _elite_selection_rate, 
                            vector<vector<double> > _dist){
                                this->population = _population;
                                this->max_generations = _max_generations;
                                this->crossover_probability = _crossover_probability;
                                this->mutation_probability = _mutation_probability;
                                this->elite_selection_rate = _elite_selection_rate;
                                this->dist = _dist;
                            }


/**
 * @brief エリート選択とルーレット選択方式で、次世代に残す子個体を選択
 * 
 * @return vector<Chromosome> 次世代に残す個体群
 */
vector<Chromosome> GeneticAlgorithm::selection(){
    //! エリート選択方式で選ばれる個体の数
    int n_elites = int(this->population.size()*this->elite_selection_rate);

    vector<Chromosome> selected_chromosomes;
    selected_chromosomes.clear();

    // エリート選択
    for(int i=0; i<n_elites; i++){
        Chromosome min = this->population[0];
        int j = 0;
        while(j < this->population.size()){
            if(this->population[j].length < min.length) min = this->population[j];
            j++;
        }
        this->population.erase(min);
        selected_chromosomes.push_back(min);
    }


    // ルーレット選択方式
    // 長さに比例した数だけindexをリストに入れ、そのリストからランダムに選ぶことで、
    // 適応度を加味したルーレット選択方式を実装しました。
    vector<int> weight;
    for(int i=0; i<this->population.size(); i++)
        for(int j=0; j<(this->population[i].length)/100; j++) weight.push_back(i); //length/100だけリストにindexを入れる
    
    for(int i=0; i<(this->population.size() - n_elites); i++)
        selected_chromosomes.push_back(this->population[rand()%this->population.size()]); // ランダムでリストから選ぶ

    return selected_chromosomes;
}


/**
 * @brief 交叉確率に基づいて、交叉
 * 
 * @param new_population 交叉後の個体群
 */
void GeneticAlgorithm::crossover(vector<Chromosome>& new_population){
    // 今回は、実装が簡単なことを優先して、2つの親から生まれた2つの個体を引き継ぐのではなく、
    // 自分と相手の遺伝子を引き継いだ1つの個体を、自分の代わりに次世代へ引き継ぐようにしました。
    for(int i=0; i<new_population.size(); i++){
        if((double)rand()/RAND_MAX < this->crossover_probability){ // 交叉確率を上回ったら
            vector<int> tmp_path = new_population[i].cyclic_crossover(new_population[rand()%(new_population.size())].path, this->dist); // ランダムに相手を選んで
            Chromosome newc; //新しい個体を生成して
            newc.init(tmp_path, this->dist); // 交叉したpathで初期化
            new_population[i] = newc;
        }
    }
}


/**
 * @brief 変異確率に基づいて、突然変異を行う
 * 
 * @param new_population 
 */
void GeneticAlgorithm::mutate(vector<Chromosome>& new_population){
    for(int i=0; i<new_population.size(); i++){
        if((double)rand()/RAND_MAX < this->mutation_probability){ // 変異確率を上回ったら
            new_population[i].swap_mutation(); // 突然変異を行い、
            new_population[i].get_path_length(this->dist); // pathの総距離を計算し直す
        }
    }
}


/**
 * @brief 次世代の個体を生成し、個体群を、生成した次世代の個体群で置換する
 * 
 */
void GeneticAlgorithm::next_generation(){
    vector<Chromosome> new_population = this->selection(); // 選択
    
    this->crossover(new_population); // 交叉
    this->mutate(new_population); // 突然変異

    this->population.clear();
    this->population = new_population;
}


/**
 * @brief 遺伝的アルゴリズムを実行し、全ての世代で最も良い個体を取得する。
 * 
 * @return vector<int> 最も良い（pathの総距離が短い）個体
 */
vector<int> GeneticAlgorithm::run_alorithm(){
    // 今回はプログラムが早く動くことを重視し、最も良い個体を最後に次世代個体群へ追加することにしました。

    Chromosome best;
    for(int i=0; i<this->max_generations; i++){
        best = this->population[0];
        for(auto c: this->population){ // 最も総距離が短かった個体をbestとする
            if(c.length < best.length) best = c;
        }
        if(!(i%100)) print_info(i, best.length);
        this->next_generation(); // 世代交代
        this->population.pop_back(); // bestが入るように末尾の個体削除
        this->population.push_back(best); // 前世代のbest個体を追加
    }

    cout << "Best length : " << best.length << endl;
    return best.path;
}


void GeneticAlgorithm::print_info(int gen, double best_length){
    double mean;
    for(int i=0; i < this->population.size(); i++) mean += this->population[i].length;
    cout << gen << "世代 Best : " << double(best_length);
    cout << "\tmean : " << mean/this->population.size() << endl;
}