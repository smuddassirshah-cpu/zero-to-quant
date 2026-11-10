// slip: n_ * o.n_ / n is a whole-number division in the merge
class RunningStats {
public:
    void add(double x) {
        ++n_;
        double d = x - mean_;
        mean_ += d / n_;
        m2_ += d * (x - mean_);
    }
    long long count() const { return n_; }
    double mean() const { return n_ ? mean_ : 0.0; }
    double variance() const { return n_ < 2 ? 0.0 : m2_ / (n_ - 1); }
    void merge(const RunningStats& o) {
        if (o.n_ == 0) return;
        if (n_ == 0) { *this = o; return; }
        long long n = n_ + o.n_;
        double d = o.mean_ - mean_;
        mean_ += d * o.n_ / n;
        m2_ += o.m2_ + (n_ * o.n_ / n) * d * d;
        n_ = n;
    }
private:
    long long n_ = 0;
    double mean_ = 0.0, m2_ = 0.0;
};
