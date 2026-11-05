// A minimal reference-counted pointer. All owners share one heap counter next to the object.
// The object is deleted, and the counter freed, when the last owner goes.
// Write: the copy and move members and the destructor. use_count() is 0 for an empty pointer.
template <typename T>
class SharedPtr {
public:
    SharedPtr() = default;
    explicit SharedPtr(T* p) : ptr_(p), count_(p ? new long(1) : nullptr) {}

    // TODO: copy constructor: share the object and add one to the count
    SharedPtr(const SharedPtr& other) : ptr_(other.ptr_), count_(other.count_) {}
    // TODO: copy assignment: let go of the old object, share the new one
    SharedPtr& operator=(const SharedPtr& other) {
        ptr_ = other.ptr_;
        count_ = other.count_;
        return *this;
    }
    // TODO: move constructor and move assignment (noexcept): take over, leave the source empty
    // TODO: destructor: subtract one; at zero delete the object and the counter
    ~SharedPtr() {}

    long use_count() const { return count_ ? *count_ : 0; }
    T* get() const { return ptr_; }
    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }

private:
    T* ptr_ = nullptr;
    long* count_ = nullptr;
};
