// A buffer of doubles on the heap. It copies correctly already.
// Add a move constructor and a move assignment: each takes the other buffer's block
// and leaves it empty (size 0). Neither may allocate, and both must be noexcept.
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

    // TODO: Buffer(Buffer&& other) noexcept
    // TODO: Buffer& operator=(Buffer&& other) noexcept

    int size() const { return size_; }
    double get(int i) const { return data_[i]; }

private:
    int size_;
    double* data_;
};
