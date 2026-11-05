#include <functional>
#include <utility>

// A scope guard runs a callback once, when it goes out of scope, unless it was dismissed.
// Write: the destructor, dismiss(), copying deleted, a noexcept move constructor that
// hands the duty to the new guard (the old one must do nothing), and assignment deleted.
class ScopeGuard {
public:
    explicit ScopeGuard(std::function<void()> f) : f_(std::move(f)), active_(true) {}
    ~ScopeGuard() {
        if (active_) f_();
    }
    void dismiss() { active_ = false; }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    ScopeGuard(ScopeGuard&& other) noexcept : f_(std::move(other.f_)), active_(other.active_) {
        other.active_ = false;
    }
    ScopeGuard& operator=(ScopeGuard&&) = delete;

private:
    std::function<void()> f_;
    bool active_;
};
