#include <vector>
using namespace std;

struct City
{
    double x;
    double y;
};

vector<City> read_input(string);
void output_file(string, vector<int>);
void print_tour(vector<int>);
vector<string> split(string, char);
vector<int> split_int(string, char);