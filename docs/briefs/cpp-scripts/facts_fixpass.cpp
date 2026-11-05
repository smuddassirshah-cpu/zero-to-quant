#include <string>
#include <vector>
#include <memory>
#include <type_traits>
#include <cstdio>
struct Pos { std::string sym; std::vector<int> lots; Pos(Pos&&) = default; Pos(const Pos&) = default; };
struct Pos3 { std::string sym; std::vector<int> lots; Pos3(Pos3&& o) : sym(std::move(o.sym)), lots(std::move(o.lots)) {} };
struct Fill {};
struct Order { std::unique_ptr<Fill> fill; ~Order() {} };
int gone = 0;
struct Base { ~Base() {} };
struct Derived : Base { std::vector<double> v; ~Derived() { ++gone; } };
int main() {
  std::printf("%d %d\n", (int)std::is_nothrow_move_constructible_v<Pos>, (int)std::is_nothrow_move_constructible_v<Pos3>);
  std::printf("order move %d copy %d\n", (int)std::is_move_constructible_v<Order>, (int)std::is_copy_constructible_v<Order>);
  { std::shared_ptr<Base> p = std::make_shared<Derived>(); p.reset(); }
  std::printf("gone %d\n", gone);
  std::string s = "ab"; char c = s[s.size()]; std::printf("c=%d\n", (int)c);
  unsigned char b = 255; ++b; std::printf("b=%d\n", (int)b);
}
