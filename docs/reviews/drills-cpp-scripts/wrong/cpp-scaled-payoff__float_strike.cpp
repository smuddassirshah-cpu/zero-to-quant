// slip: float for double in the forward's strike
#include <memory>
#include <utility>

class Forward : public Payoff {
public:
    explicit Forward(double k) : k_(k) {}
    double operator()(double spot) const override { return spot - k_; }
private:
    float k_;
};

class Scaled : public Payoff {
public:
    Scaled(double qty, std::unique_ptr<Payoff> inner) : qty_(qty), inner_(std::move(inner)) {}
    double operator()(double spot) const override { return qty_ * (*inner_)(spot); }
private:
    double qty_;
    std::unique_ptr<Payoff> inner_;
};
