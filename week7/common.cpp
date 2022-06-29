#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <set>
#include <random>
#include "common.h"

using namespace std;


/**
 * @brief 座標ファイルを読み込む。
 * 
 * @param fname ファイル名
 * @return vector<City> 各都市の座標(City)のリスト
 */
vector<City> read_input(string fname){
    vector<City> cities;

    ifstream ifs(fname);
    string line;
    getline(ifs, line); //1行目

    //1行ずつファイルを見ていく
    while (getline(ifs, line)){
        vector<string> xy = split(line, ',');
        City city;
        city.x = stod(xy[0]);
        city.y = stod(xy[1]);
        cities.push_back(city);
    }
    return cities;
}


/**
 * @brief 経路をファイルに出力する。
 * 
 * @param fname ファイル名
 * @param path 経路
 */
void output_file(string fname, vector<int> path){
    ofstream ofs(fname); 
    ofs << "index" << endl;
    for(int i=0; i<path.size(); i++) ofs << to_string(path[i]) << endl;
    ofs.close();
}


/**
 * @brief 結果を出力する。
 * 
 * @param tour 経路
 */
void print_tour(vector<int> tour){
    for(int i=0; i<tour.size(); i++)
        printf("%d\n", tour[i]);
}


/**
 * @brief 与えられた文字列を指定された文字で区切る。
 * 
 * @param str 対象の文字列
 * @param del 区切り文字
 * @return vector<string> 
 */
vector<string> split(string str, char del) {
    int first = 0;
    int last = str.find_first_of(del);
    vector<string> result;

    while (first < str.size()) {
        // strの(first)文字目から、(last-first)文字をtmpに代入
        string tmp(str, first, last-first);
 
        result.push_back(tmp);
 
        first = last + 1;
        last = str.find_first_of(del, first);
        if (last == string::npos) {
            last = str.size();
        }
    }
    return result;
}


/**
 * @brief 与えられた文字列を指定された文字で区切り、int型のvectorを返す。
 * 
 * @param str 対象の文字列
 * @param del 区切り文字
 * @return vector<int> 
 */
vector<int> split_int(string str, char del) {
    int first = 0;
    int last = str.find_first_of(del);
    vector<int> result;

    while (first < str.size()) {
        // strの(first)文字目から、(last-first)文字をtmpに代入
        string tmp(str, first, last-first);
 
        result.push_back(stoi(tmp));
 
        first = last + 1;
        last = str.find_first_of(del, first);
        if (last == string::npos) {
            last = str.size();
        }
    }
    return result;
}

