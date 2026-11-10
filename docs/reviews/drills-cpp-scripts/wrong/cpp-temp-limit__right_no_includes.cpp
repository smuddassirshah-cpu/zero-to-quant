// right: the model without the two includes the class itself does not need
class TempLimit {
public:
    TempLimit(int& limit, int cap) : limit_(limit), old_(limit) {
        if (cap < limit_) limit_ = cap;
    }
    ~TempLimit() { limit_ = old_; }
    TempLimit(const TempLimit&) = delete;
    TempLimit& operator=(const TempLimit&) = delete;
private:
    int& limit_;
    int old_;
};
