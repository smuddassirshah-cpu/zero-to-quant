// slip: std::move on a const reference still copies
void take_all(std::vector<Fill>& dst, std::vector<Fill>&& src) {
    for (const Fill& f : src) dst.push_back(std::move(f));
    src.clear();
}
