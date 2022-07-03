/**
 * Google STEP Class 7 Homework
 * 
 * 行列積のループ順序としては6種類の組合せがある。
 * この6種類を実行速度が速いと思う方から順に並べてください。
 * 実際に実験してその予想が正しいかどうか確かめてください。
 * 
 * 実行方法：
 * g++ -o martix matrix.cpp -std=c++11
 * ./matrix N
 */


#include <iostream>
#include <vector>
#include <time.h>
#include <string>

using namespace std;

int main(int argc, char *argv[]){

    if(argc != 2){ 
		cout << "Usage: " << argv[0] << " N" << endl;
        return -1;
    }
    int n = stoi(argv[1]);
    double* a = (double*)malloc(n * n * sizeof(double)); // Matrix A
    double* b = (double*)malloc(n * n * sizeof(double)); // Matrix B
    double* c = (double*)malloc(n * n * sizeof(double)); // Matrix C

    int i, j, k;
    clock_t begin, end;
    vector<double> times;
    vector<string> loops = {"i-j-k", "i-k-j", "j-i-k", "j-k-i", "k-i-j", "k-j-i"};

    // Initialize the matrices to some values.
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            a[i * n + j] = i * n + j; // A[i][j]
            b[i * n + j] = j * n + i; // B[i][j]
            c[i * n + j] = 0; // C[i][j]
        }
    }

    //i-j-k 
    begin = clock();
    for(i = 0; i < n; i++)
        for(j = 0; j < n; j++)
            for(k = 0; k < n; k++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);

    //i-k-j 
    begin = clock();
    for(i = 0; i < n; i++)
        for(k = 0; k < n; k++)
            for(j = 0; j < n; j++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);


    //j-i-k
    begin = clock();
    for(j = 0; j < n; j++)
        for(i = 0; i < n; i++)
            for(k = 0; k < n; k++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);

    //j-k-i
    begin = clock();
    for(j = 0; j < n; j++)
        for(k = 0; k < n; k++)
            for(i = 0; i < n; i++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);

    //k-i-j
    begin = clock();
    for(k = 0; k < n; k++)
        for(i = 0; i < n; i++)
            for(j = 0; j < n; j++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);

    //k-j-i
    begin = clock();
    for(k = 0; k < n; k++)
        for(j = 0; j < n; j++)
            for(i = 0; i < n; i++)
                c[i * n + j] += a[i * n + k] * b[k * n + j];
    end = clock();
    times.push_back(end - begin);

    for(int i = 0; i<6; i++){
        cout << loops[i] << " time: " << times[i]/CLOCKS_PER_SEC << "sec" << endl;

    }

    // Print C for debugging. Comment out the print before measuring the execution time.
    /*
    double sum = 0;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
        sum += c[i * n + j];
        // printf("c[%d][%d]=%lf\n", i, j, c[i * n + j]);
        }
    }
    // Print out the sum of all values in C.
    // This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
    printf("sum: %.6lf\n", sum);
    */
    return 0;

}