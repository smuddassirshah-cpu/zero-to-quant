// slip: one number reader for both fields, so a price with a leading minus is accepted
#include <string>

bool read_whole(const std::string& s, long long& out) {
    std::size_t i = 0;
    bool neg = false;
    if (!s.empty() && s[0] == '-') { neg = true; i = 1; }
    if (i == s.size()) return false;
    long long v = 0;
    for (; i < s.size(); ++i) {
        if (s[i] < '0' || s[i] > '9') return false;
        v = v * 10 + (s[i] - '0');
    }
    out = neg ? -v : v;
    return true;
}

long long row_value(const std::string& line) {
    std::string qty, price;
    int commas = 0;
    for (char c : line) {
        if (c == ',') ++commas;
        else if (commas == 0) qty += c;
        else price += c;
    }
    long long q = 0, p = 0;
    if (commas != 1 || !read_whole(qty, q) || !read_whole(price, p)) return 0;
    return q * p;
}

long long fills_value(const std::string& text) {
    long long total = 0;
    std::string line;
    for (std::size_t i = 0; i <= text.size(); ++i) {
        if (i == text.size() || text[i] == '\n') {
            if (!line.empty() && line.back() == '\r') line.pop_back();
            total += row_value(line);
            line.clear();
        } else {
            line += text[i];
        }
    }
    return total;
}
