// slip: the raw count is stored and wrapped only when read; operator< compares the raw counts
class SessionTime {
public:
    explicit SessionTime(int minutes) : m_(minutes) {}
    int minutes() const { return ((m_ % 1440) + 1440) % 1440; }
    friend bool operator<(SessionTime a, SessionTime b) { return a.m_ < b.m_; }
private:
    int m_;
};

SessionTime operator+(SessionTime t, int m) { return SessionTime(t.minutes() + m); }
int operator-(SessionTime b, SessionTime a) { return SessionTime(b.minutes() - a.minutes()).minutes(); }
