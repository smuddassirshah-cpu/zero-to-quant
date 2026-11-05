// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0, data() null). Neither may allocate, and both must be noexcept.
// The move assignment must be safe for `a = std::move(a)`.
class Buffer {
public:
    Buffer(int n, double x) : size_(n), data_(new double[n]) {
        for (int i = 0; i < n; ++i) data_[i] = x;
    }
    Buffer(const Buffer& other) : size_(other.size_), data_(new double[other.size_]) {
        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            double* fresh = new double[other.size_];
            for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
            delete[] data_;
            data_ = fresh;
            size_ = other.size_;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }
    const double* data() const { return data_; }

private:
    int size_;
    double* data_;
};
