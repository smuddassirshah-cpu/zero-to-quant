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

    Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Samples& operator=(const Samples& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    void set(int i, double x) { data_[i] = x; }

private:
    int size_;
    double* data_;
};
