/**
 * Google STEP Class 7 Homework
 * 〜帰ってきたTSP Challenge〜
 * 
 * Method 1: Greedy + 3-opt
 * 
 * 実行方法：
 * g++ -o solver_3opt solver_3opt.cpp common.cpp
 * ./solver_3opt
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <set>
#include <random>
#include "common.h"

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
 * @brief 貪欲法で経路を求める。
 * 
 * @param cities 各都市の座標のリスト
 * @param current_city 貪欲法を始める点
 * @param dist 各都市間の距離のリスト
 * @return vector<int> 経路
 */
vector<int> greedy(vector<City> cities, int current_city, vector<vector<double> > dist){
    
    set<int> unvisited_cities;
    for(int i=0; i < N; i++) unvisited_cities.insert(i); //0~N-1までの数字を入れておく
    unvisited_cities.erase(current_city); //始点を集合から削除

    vector<int> tour;
    tour.push_back(current_city); //始点をtourに入れる

    while(!unvisited_cities.empty()){
        int next_city = -1;
        // unvisited_citiesの中で、current_cityから最も距離が近い都市をnext_cityに入れる
        for(auto c : unvisited_cities)
            if(dist[current_city][c] < dist[current_city][next_city] || next_city < 0)
                next_city = c;

        unvisited_cities.erase(next_city); // 訪問済みにして
        tour.push_back(next_city); // tourに入れて
        current_city = next_city; // 次の都市に進む
    }
    return tour;
}


/**
 * @brief リストtourの、x番目からy番目を逆順に入れ替える。
 * 
 * @param tour 経路
 * @param x 始点
 * @param y 終点
 * @return vector<int> 逆順に入れ替えたリスト
 */
vector<int> reverse_tour(vector<int> tour, int x, int y){
    while (x < y){
        swap(tour[x], tour[y]);
        x++; y--;
        if(x > N-1) x = 0;
        if(y < 0) y = N-1;
    } 
    return tour;
}



/**
 * @brief 2-optで経路を求める。
 * 
 * @param tour 経路
 * @param dist 各都市間の距離のリスト
 * @return vector<int> 2-optを適応した後の経路
 */
vector<int> two_opt(vector<int> tour,  vector<vector<double> > dist){
    bool is_change;
    while(1){
        is_change = false;
        for(int i=0; i<N-2; i++){
            for(int j=i+2; j<N; j++){
                double l1 = dist[tour[i]][tour[i+1]];
                double l2 = dist[tour[j]][tour[(j+1) % N]];
                double l3 = dist[tour[i]][tour[j]];
                double l4 = dist[tour[i+1]][tour[(j+1) % N]];
                if(l1+l2 > l3+l4){ // もし入れ替えた方が短かったら
                    tour = reverse_tour(tour, i+1, j); // i+1からjを逆順にする
                    is_change = true;
                }
            }
        }
        if(!is_change) break;
    }
    return tour;
}


/**
 * @brief 3-optで経路を求める。
 * 
 * @param tour 経路
 * @param dist 各都市間の距離のリスト
 * @return vector<int> 3-optを適応した後の経路
 */
vector<int> three_opt(vector<int> tour,  vector<vector<double> > dist){
    bool is_change;
    while(1){
        is_change = false;
        vector<int> tmp;
        for(int i=0; i<N-2; i++){
            for(int j=i+1; j<N-1; j++){
                for(int k=j+1; k<N; k++){
                    int A = tour[i], B = tour[i + 1], C = tour[j], D = tour[j + 1], E = tour[k], F = tour[(k + 1)%N];
                    double dist0 = dist[A][B] + dist[C][D] + dist[E][F];
                    double dist1 = dist[A][C] + dist[B][D] + dist[E][F];
                    double dist2 = dist[A][B] + dist[C][E] + dist[D][F];
                    double dist3 = dist[A][D] + dist[E][B] + dist[C][F];
                    double dist4 = dist[F][B] + dist[C][D] + dist[E][A];
                    if(dist0 > dist1){
                        tour = reverse_tour(tour, i+1, j);
                        is_change = true;
                    }else if(dist0 > dist2){
                        tour = reverse_tour(tour, j+1, k);
                        is_change = true;
                    }else if(dist0 > dist4){
                        tour = reverse_tour(tour, i+1, k);
                        is_change = true;
                    }else if(dist0 > dist3){
                        tmp.clear();
                        //tour[:i+1] + tour[j+1:k+1] + tour[i+1:j+1] + tour[k+1:]にする。
                        for(int z = 0; z < i+1; z++) tmp.push_back(tour[z]);
                        for(int z = j+1; z < k+1; z++) tmp.push_back(tour[z%N]);
                        for(int z = i+1; z < j+1; z++) tmp.push_back(tour[z]);
                        for(int z = k+1; z < N; z++) tmp.push_back(tour[z%N]);
                        tour = tmp;
                        is_change = true;
                    }
                }
            }
        }
        if(!is_change) break;
    }
    return tour;
}


/**
 * @brief greedy -> 3-opt でTSPを解く。
 * 
 * @param cities 各都市の座標が入ったリスト
 */
void solve(vector<City> cities){

    int population_size = 1; // 生成する経路の数

    vector<vector<double> > dist = make_dist(cities);
    vector<int> best_path, tmp_path;
    float best_length = INT_MAX, tmp_length = 0;

    int init_city = rand()%N; // 最初の始点はランダムで決める

    for(int i=0; i<population_size; i++){
        double longest = -1.0;
        tmp_path = greedy(cities, init_city, dist); // greedy
        tmp_path = three_opt(tmp_path, dist); // 3-opt
        //tmp_path = two_opt(tmp_path, dist); // 2-opt
        for(int j=0; j<N; j++){        
            tmp_length += dist[tmp_path[j]][tmp_path[(j+1)%N]]; // 各辺の長さを足していく
            if(dist[tmp_path[j]][tmp_path[(j+1)%N]] > longest){ // 同時に一番長い辺を見つけて、次はその点を視点にする
                init_city = j;
                longest = dist[tmp_path[j]][tmp_path[(j+1)%N]];
            }
        }
        cout << i << " : " << tmp_length << endl;
        if(tmp_length < best_length){
            best_length = tmp_length;
            best_path = tmp_path;
        }
        tmp_length = 0;
    }

    cout << "Best length : " << best_length << endl;

    // 結果のpathをcsvファイルに残す
    string output_filename = "3opt_" + to_string(N) + ".csv";
    output_file(output_filename, best_path);
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