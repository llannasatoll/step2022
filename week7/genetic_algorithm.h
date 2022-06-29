#include <vector>

using namespace std;


class Chromosome
{
    public:
    vector<int> path;
    double length;
    void init(vector<int>, vector<vector<double> >);
    vector<int> cyclic_crossover(vector<int>, vector<vector<double> >);
    void swap_mutation();
    void get_path_length(vector<vector<double> >);
};


class GeneticAlgorithm
{
    public:
    vector<Chromosome> population;
    int max_generations;
    float crossover_probability;
    float mutation_probability;
    float elite_selection_rate;
    vector<vector<double> > dist;

    void init(vector<Chromosome>, int, float, float, float, vector<vector<double> >);
    vector<Chromosome> selection();
    void crossover(vector<Chromosome>&);
    void mutate(vector<Chromosome>&);
    void next_generation();
    vector<int> run_alorithm();
    void print_info(int, double);
};