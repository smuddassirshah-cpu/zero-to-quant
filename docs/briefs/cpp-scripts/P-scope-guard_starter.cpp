#include <functional>
#include <utility>

// A scope guard runs a callback once, when it goes out of scope, unless it was dismissed.
// Write: the destructor, dismiss(), copying deleted, a noexcept move constructor that
// hands the duty to the new guard (the old one must do nothing), and assignment deleted.
class ScopeGuard {
public:
    explicit ScopeGuard(std::function<void()> f) : f_(std::move(f)), active_(true) {}
    // TODO: destructor
    void dismiss() {}                    // TODO: the callback will not run
    // TODO: copying deleted; move constructor; assignment deleted

private:
    std::function<void()> f_;
    bool active_;
};
