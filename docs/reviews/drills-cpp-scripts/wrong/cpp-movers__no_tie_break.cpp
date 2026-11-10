// slip: sorts by the move alone and trusts the map's alphabetical order to survive std::sort
#include <algorithm>
#include <cmath>
#include <map>
#include <string>
#include <utility>
#include <vector>

std::vector<std::string> movers(const std::vector<std::string>& syms, const std::vector<double>& px, double pct) {
    std::map<std::string, std::pair<double, double>> seen;
    for (std::size_t i = 0; i < syms.size(); ++i) {
        auto it = seen.find(syms[i]);
        if (it == seen.end()) seen.emplace(syms[i], std::make_pair(px[i], px[i]));
        else it->second.second = px[i];
    }
    std::vector<std::pair<double, std::string>> keep;
    for (const auto& [sym, p] : seen) {
        double move = std::abs(p.second - p.first);
        if (move * 100 >= pct * p.first) keep.push_back({move / p.first, sym});
    }
    std::sort(keep.begin(), keep.end(), [](const auto& a, const auto& b) { return a.first > b.first; });
    std::vector<std::string> out;
    for (const auto& k : keep) out.push_back(k.second);
    return out;
}
