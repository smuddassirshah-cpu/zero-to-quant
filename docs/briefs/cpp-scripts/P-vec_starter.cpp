#include <cstddef>
#include <new>
#include <utility>

// A growing array of T. T need not be default constructible or assignable, so keep raw
// storage from ::operator new and build elements in it with placement new.
// Growth: capacity 0 to start (no allocation), 1 on the first push, then doubling.
// push_back must work when its argument lives inside the vector (v.push_back(v[0])).
// Growth moves elements if T's move constructor is noexcept (std::move_if_noexcept).
template <typename T>
class Vec {
public:
    Vec() = default;
    // TODO: destructor (destroy every element, then free the block)
    // TODO: copy constructor and copy assignment
    // TODO: move constructor and move assignment (noexcept)
    void push_back(const T& x) { (void)x; }       // TODO
    void push_back(T&& x) { (void)x; }            // TODO

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
