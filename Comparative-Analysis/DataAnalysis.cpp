#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <chrono>
#include <cmath>
#include <map>
#include <iomanip>
#include <algorithm>
#include <windows.h>
#include <psapi.h>
#pragma comment(lib, "Psapi.lib")
using namespace std;
using namespace chrono;
struct Stats {
    vector<double> values;
    double avg = 0, max = 0, min = 0, stddev = 0;
    string trend = "N/A";
};
double calc_mean(const vector<double>& v) {
    double sum = 0;
    for (double val : v) sum += val;
    return sum / v.size();
}
double calc_stddev(const vector<double>& v, double mean) {
    double sq = 0;
    for (double val : v) sq += (val - mean) * (val - mean);
    return sqrt(sq / v.size());
}
double getMemoryUsageMB() {
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        return static_cast<double>(pmc.WorkingSetSize) / (1024 * 1024); // Convert bytes to MB
    }
    return 0.0;
}
int main() {
    ifstream file("indiavix.csv");
    if (!file.is_open()) {
        cerr << "Failed to open file.\n";
        return 1;
    }
    string line;
    map<int, Stats> yearly_data;
    getline(file, line); // skip header
    auto start_time = high_resolution_clock::now();
    double mem_before = getMemoryUsageMB();
    while (getline(file, line)) {
        stringstream ss(line);
        string date, value;
        getline(ss, date, ',');  // Date
        getline(ss, value, ','); // Close (VIX value)
        try {
            double vix = stod(value);
            int year = stoi(date.substr(0, 4));
            if (year >= 2009 && year <= 2021) {
                yearly_data[year].values.push_back(vix);
            }
        }
        catch (...) {
        }
    }
    double prev_avg = 0;
    for (auto it = yearly_data.begin(); it != yearly_data.end(); ++it) {
        int year = it->first;
        Stats& stats = it->second;
        vector<double>& vals = stats.values;
        if (vals.empty()) continue;
        stats.avg = calc_mean(vals);
        stats.stddev = calc_stddev(vals, stats.avg);
        stats.max = *max_element(vals.begin(), vals.end());
        stats.min = *min_element(vals.begin(), vals.end());
        if (prev_avg != 0) {
            if (stats.avg > prev_avg)
                stats.trend = "↑ Up";
            else if (stats.avg < prev_avg)
                stats.trend = "↓ Down";
            else
                stats.trend = "→ Flat";
        }
        prev_avg = stats.avg;
    }
    auto end_time = high_resolution_clock::now();
    double mem_after = getMemoryUsageMB();
    duration<double> exec = end_time - start_time;
    cout << fixed << setprecision(2);
    cout << "Execution Time: " << exec.count() << "s\n";
    cout << "Memory Used: " << (mem_after - mem_before) << " MB\n\n";
    cout << "Yearly India VIX Summary (2009–2021):\n";
    cout << "Year  AvgVIX  MaxVIX  MinVIX  StdDev  Trend\n";
    for (auto it = yearly_data.begin(); it != yearly_data.end(); ++it) {
        int year = it->first;
        const Stats& stats = it->second;
        cout << year << "  "
            << setw(7) << stats.avg << "  "
            << setw(7) << stats.max << "  "
            << setw(7) << stats.min << "  "
            << setw(7) << stats.stddev << "  "
            << stats.trend << "\n";
    }
    return 0;
}