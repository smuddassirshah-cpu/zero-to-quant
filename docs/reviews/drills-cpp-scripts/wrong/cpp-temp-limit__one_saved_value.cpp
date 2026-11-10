// slip: the old value is kept in one static shared by every object, so nested blocks overwrite it
#include <memory>
#include <vector>

class TempLimit {
public:
    TempLimit(int& limit, int cap) : limit_(limit) {
        old_ = limit;
        if (cap < limit_) limit_ = cap;
    }
    ~TempLimit() { limit_ = old_; }
    TempLimit(const TempLimit&) = delete;
    TempLimit& operator=(const TempLimit&) = delete;
private:
    int& limit_;
    static int old_;
};
int TempLimit::old_ = 0;
