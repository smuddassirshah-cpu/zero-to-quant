// A minimal unique pointer. It owns one heap object, or nothing.
// Write: the destructor; copying deleted; a move constructor and move assignment that
// transfer ownership and leave the source empty; release(); reset().
template <typename T>
class UniquePtr {
public:
    UniquePtr() = default;
    explicit UniquePtr(T* p) : ptr_(p) {}

    ~UniquePtr() { delete ptr_; }
    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    UniquePtr(UniquePtr&& other) noexcept : ptr_(other.ptr_) { other.ptr_ = nullptr; }
    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }

    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    T* release() {
        T* p = ptr_;
        ptr_ = nullptr;
        return p;
    }
    void reset(T* p = nullptr) {
        T* old = ptr_;
        ptr_ = p;
        delete old;
    }

private:
    T* ptr_ = nullptr;
};
