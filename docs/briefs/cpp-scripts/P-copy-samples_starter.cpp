#include <utility>

// Samples owns a heap array of doubles. The destructor and the two move members are done.
// The copy constructor and copy assignment are wrong: they copy the pointer, so two objects
// would free one block. Make each a true copy of the doubles.
// Copy assignment must free the old block, be safe for `a = a`, and return *this.
class Samples {
public:
    Samples(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    ~Samples() { delete[] data_; }
    Samples(Samples&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Samples& operator=(Samples&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    // TODO: copy the doubles, not the pointer
    Samples(const Samples& other) : size_(other.size_), data_(other.data_) {}
    // TODO: free the old block, copy the doubles, guard against a = a, return *this
    Samples& operator=(const Samples& other) {
        size_ = other.size_;
        data_ = other.data_;
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    void set(int i, double x) { data_[i] = x; }

private:
    int size_;
    double* data_;
};
