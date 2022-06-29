/**
 * Google STEP Class 7 Homework
 * 〜帰ってきたTSP Challenge〜
 * 
 * 
 * 深さ優先探索で経路を探す。
 * makefile_for_dfs.ipynbで作成した、link_(n).txtが必要になる。
 * 
 * 実行方法：
 * g++ -o solver_dfs solver_dfs.cpp
 * ./solver_dfs
 * 
 * その後、
 * Challenge number(0~7): 
 * と出力されるので、0~7の数字を入力する。
 * 
 * 出力：dfs_(n).csv
 */


#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include "common.h"

using namespace std;

int N;
int n_links;

/**
 * @brief 深さ優先探索で経路を探す
 * 
 * @param current_city 現在の点
 * @param links 各点の繋がりを表したリスト
 * @param visited 訪問済みリスト
 * @return vector<int> 一周できるルートが見つかったら返す
 */
vector<int> dfs(int current_city, vector<vector<int> >& links, vector<int> visited){
    vector<int> ans;
    visited.push_back(current_city); // 現在の点を訪問済みにする

    if(visited.size() == N){ // 全ての点を見たら経路完成
        ans.push_back(current_city);
        return ans;
    }

    for(int i=0; i<n_links; i++){
        if(find(visited.begin(), visited.end(), links[current_city][i]) == visited.end()){ // 次の点が探索済みじゃなかったら
            vector<int> tmp = dfs(links[current_city][i], links, visited); // 再帰呼び出し
            if(!tmp.empty()){// 先でpathが見つかっていたら
                tmp.push_back(current_city);
                return tmp;
            }
        }
    }
    return ans; // なかったら空リストを返す
}


int main(){
    int n_challenge;
    cout << "Challenge number(0~7): ";
    cin >> n_challenge;

    string fname = "link_" + to_string(n_challenge) + ".txt";
    ifstream ifs(fname);
    string line;

    // 1行目に都市数N、2行目に各点から繋がっている都市数n_links
    getline(ifs, line);
    N = stoi(line);
    getline(ifs, line);
    n_links = stoi(line);

    // i番目と繋がっている点のリストがlinks[i]
    vector<vector<int> > links(N, vector<int>(n_links));
    int i = 0, j = 0;
    while (getline(ifs, line)){
        vector<int> tmp_list = split_int(line, ',');
        while (j < tmp_list.size()){
            links[i][j] = tmp_list[j];
            j++;
        }
        i++;
        j = 0;
    }

    vector<int> visited;
    vector<int> ans = dfs(0, links, visited);

    // 結果出力
    if(!ans.empty()){
        cout << "Found!\n";
        string output_filename = "dfs_" + to_string(n_challenge) + ".csv";
        ofstream ofs(output_filename); 
        ofs << "index" << endl;
        for(int i=0; i<ans.size(); i++) ofs << to_string(ans[i]) << endl;
        ofs.close();
    }
}