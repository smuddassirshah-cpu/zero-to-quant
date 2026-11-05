// A minimal reference-counted pointer. All owners share one heap counter next to the object.
// The object is deleted, and the counter freed, when the last owner goes.
// Write: the copy and move members and the destructor. use_count() is 0 for an empty pointer.
template <typename T>
class SharedPtr {
public:
    SharedPtr() = default;
    explicit SharedPtr(T* p) : ptr_(p), count_(p ? new long(1) : nullptr) {}

    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {
        if (count_) ++*count_;
    }
    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;
    }
    SharedPtr(SharedPtr&& other) noexcept : ptr_(other.ptr_), count_(other.count_) {
        other.ptr_ = nullptr;
        other.count_ = nullptr;
    }
    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;
    }
    ~SharedPtr() { drop(); }

    long use_count() const { return count_ ? *count_ : 0; }
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }

private:
    void drop() {
        if (count_ && --*count_ == 0) {
            delete ptr_;
            delete count_;
        }
        ptr_ = nullptr;
        count_ = nullptr;
    }
    T* ptr_ = nullptr;
    long* count_ = nullptr;
};
