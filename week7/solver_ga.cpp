/**
 * Google STEP Class 7 Homework
 * 〜帰ってきたTSP Challenge〜
 * 
 * Method 1: Greedy + 3-opt + 2-opt
 * Method 2: Genetic Algorithm
 * 
 * 実行方法：
 * g++ -o solver_ga solver_ga.cpp common.cpp genetic_algorithm.cpp
 * ./solver_ga
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <set>
#include <random>
#include "common.h"
#include "genetic_algorithm.h"

using namespace std;

int N;
vector<int> ans;

/**
 * @brief 2都市間の距離を求める。
 * 
 * @param city1 
 * @param city2 
 * @return double 
 */
double distance(City city1, City city2){
    return sqrt((city1.x - city2.x)*(city1.x - city2.x) + (city1.y - city2.y)*(city1.y - city2.y));
}


/**
 * @brief 各都市間の座標の距離を計算したリストを作成する。
 * 
 * @param cities 各都市の座標のリスト
 * @return vector<vector<double> > 経路
 */
vector<vector<double> > make_dist(vector<City> cities){
    //! N×N のdoubleの配列の宣言
    vector<vector<double> > dist(N, vector<double>(N));
    for (int i = 0; i < N; i++)
        for (int j = i; j < N; j++)
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j]);

    return dist;
}


/**
 * @brief Genetic AlgorithmでTSPを解く。初期個体群はランダムに生成。
 * 
 * @param cities 各都市の座標が入ったリスト
 */
void solve(vector<City> cities){

    int population_size = 20; // 世代の個体群
    int max_generations = 10000; // 最大世代数
    float crossover_probability = 0.8; // 交叉確率（0~1）
    float mutation_probability = 0.3; // 変異確率（0~1）
    float elite_selection_rate = 0.3; // エリート選択方式で選ばれる個体の割合（0~1）

    vector<vector<double> > dist = make_dist(cities);
    vector<Chromosome> initial_population;

    vector<int> path;
    for(int i=0; i<cities.size(); i++) path.push_back(i); // 0 ~ N-1 の数字が入ったリストpathを作成

    // 初期個体群生成
    for(int i=0; i<population_size; i++){
        random_device get_rand_dev;
        mt19937 get_rand_mt(get_rand_dev());
        shuffle(path.begin(), path.end(), get_rand_mt); // pathをシャッフルして
        Chromosome newc; // 新しいインスタンスを作成し
        newc.init(path, dist); // 初期化
        initial_population.push_back(newc); // 初期個体群へ追加
    }

    GeneticAlgorithm ga;
    ga.init(initial_population,
            max_generations, 
            crossover_probability, 
            mutation_probability, 
            elite_selection_rate, 
            dist);
    
    string output_filename = "ga_" + to_string(N) + ".csv";
    output_file(output_filename, ga.run_alorithm());
}


int main(int argc, char *argv[]){
    if(argc != 2){ 
        cout << "Usage: " << argv[0] << " filename" << endl;
        return -1;
    }

    vector<City> cities = read_input(argv[1]);
    N = cities.size();

    solve(cities);
    return 0;
}