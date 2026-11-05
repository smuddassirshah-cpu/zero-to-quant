// A minimal unique pointer. It owns one heap object, or nothing.
// Write: the destructor; copying deleted; a move constructor and move assignment that
// transfer ownership and leave the source empty; release(); reset().
template <typename T>
class UniquePtr {
public:
    UniquePtr() = default;
    explicit UniquePtr(T* p) : ptr_(p) {}

    // TODO: destructor
    // TODO: delete copying; write the move constructor and move assignment

    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    T* release() { return nullptr; }                 // TODO: give up ownership, do not delete
    void reset(T* p = nullptr) { (void)p; }          // TODO: delete the current object, then own p

private:
    T* ptr_ = nullptr;
};
