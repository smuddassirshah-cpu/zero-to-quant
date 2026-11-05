#include <cstddef>
#include <new>
#include <utility>

// A growing array of T. T need not be default constructible or assignable, so keep raw
// storage from ::operator new and build elements in it with placement new.
// Growth: capacity 0 to start (no allocation), 1 on the first push, then doubling.
// push_back must work when its argument lives inside the vector (v.push_back(v[0])).
// Copy assignment must be safe for `a = a`.
// Write both push_back overloads, or share a helper: a template parameter `U&&` accepts both,
// and std::forward<U>(x) passes it on as a copy or a move.
// Growth moves elements if T's move constructor is noexcept (std::move_if_noexcept).
template <typename T>
class Vec {
public:
    Vec() = default;
    ~Vec() { destroy(); }

    Vec(const Vec& other) : size_(other.size_), cap_(other.size_), data_(allocate(other.size_)) {
        for (std::size_t i = 0; i < size_; ++i) new (data_ + i) T(other.data_[i]);
    }
    Vec& operator=(const Vec& other) {
        if (this != &other) {
            Vec copy(other);
            swap(copy);
        }
        return *this;
    }
    Vec(Vec&& other) noexcept : size_(other.size_), cap_(other.cap_), data_(other.data_) {
        other.size_ = 0;
        other.cap_ = 0;
        other.data_ = nullptr;
    }
    Vec& operator=(Vec&& other) noexcept {
        if (this != &other) {
            destroy();
            size_ = other.size_;
            cap_ = other.cap_;
            data_ = other.data_;
            other.size_ = 0;
            other.cap_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }

    void push_back(const T& x) { emplace(x); }
    void push_back(T&& x) { emplace(std::move(x)); }

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T& operator[](std::size_t i) { return data_[i]; }
    const T& operator[](std::size_t i) const { return data_[i]; }

private:
    static T* allocate(std::size_t n) {
        return n ? static_cast<T*>(::operator new(n * sizeof(T))) : nullptr;
    }
    void destroy() {
        for (std::size_t i = 0; i < size_; ++i) data_[i].~T();
        ::operator delete(data_);
        size_ = 0;
        cap_ = 0;
        data_ = nullptr;
    }
    void swap(Vec& o) {
        std::swap(size_, o.size_);
        std::swap(cap_, o.cap_);
        std::swap(data_, o.data_);
    }
    template <typename U>
    void emplace(U&& x) {
        if (size_ == cap_) {
            std::size_t new_cap = cap_ ? cap_ * 2 : 1;
            T* fresh = allocate(new_cap);
            new (fresh + size_) T(std::forward<U>(x));      // x may live in the old block, so build it first
            for (std::size_t i = 0; i < size_; ++i) {
                new (fresh + i) T(std::move_if_noexcept(data_[i]));
                data_[i].~T();
            }
            ::operator delete(data_);
            data_ = fresh;
            cap_ = new_cap;
        } else {
            new (data_ + size_) T(std::forward<U>(x));
        }
        ++size_;
    }

    std::size_t size_ = 0;
    std::size_t cap_ = 0;
    T* data_ = nullptr;
};
