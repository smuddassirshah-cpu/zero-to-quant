// The exact proposed cpp fixes (CP5-1 to CP5-3), applied to a SCRATCH copy of app/ for testing in the real engine.
// node fix14.mjs <scratch app dir> [--old-solutions]   (--old-solutions keeps the shipped model code with the new tests,
// to prove in the app's clang that the new tests catch it). Refuses to touch the worktree's own app/.
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const own = path.resolve(here, '../../../app');
const dir = path.resolve(process.argv[2] || '');
const OLD = process.argv.includes('--old-solutions');
if (!process.argv[2] || dir === own || !fs.existsSync(path.join(dir, 'content'))) { console.error('give a scratch copy of app/'); process.exit(2); }
const C = path.join(dir, 'content/courses/cpp');
const rd = (f) => JSON.parse(fs.readFileSync(path.join(C, f), 'utf8'));
const wr = (f, j) => fs.writeFileSync(path.join(C, f), JSON.stringify(j, null, 2) + '\n');
const rep = (s, a, b) => { const n = s.split(a).length - 1; if (n !== 1) throw new Error('anchor found ' + n + ' times: ' + a.slice(0, 60)); return s.replace(a, b); };

/* ---- CP5-1: l23 screens[2] UniquePtr move assignment ---- */
const L = rd('l23-own-smart-pointer.json');
const s2 = L.screens[2];
const U_OLD = `    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }`;
const U_NEW = `    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            T* p = other.ptr_;      // take the source first: the old object may own it
            other.ptr_ = nullptr;
            delete ptr_;
            ptr_ = p;
        }
        return *this;
    }`;
const HEAD_OLD = '// The move assignment must be safe for `a = std::move(a)`.\n';
const HEAD_NEW = '// The move assignment must be safe for `a = std::move(a)`, and when the source lives\n// inside the object it lets go, as in a list\'s `head = std::move(head->next)`.\n';
s2.widget.starter = rep(s2.widget.starter, HEAD_OLD, HEAD_NEW);
s2.widget.solution = rep(s2.widget.solution, HEAD_OLD, HEAD_NEW);
if (!OLD) s2.widget.solution = rep(s2.widget.solution, U_OLD, U_NEW);
const LINK = (P) => `\n// Hidden: a list whose nodes own the next one.\nstruct Link {\n    static inline int live = 0;\n    int v;\n    ${P}<Link> next;\n    explicit Link(int x) : v(x) { ++live; }\n    ~Link() { --live; }\n};\n`;
s2.widget.postlude = LINK('UniquePtr');
const t2 = s2.widget.tests;
s2.widget.tests = [t2[0], t2[1],
  { setup: 'UniquePtr<Tracked> a(new Tracked(1)); UniquePtr<Tracked> b = std::move(a);', call: 'b->v * 10 + (a.get() == nullptr ? 1 : 0)', expect: 11, compare: 'equal' },
  ...t2.slice(4),
  { setup: 'UniquePtr<Link> h(new Link(1)); h->next = UniquePtr<Link>(new Link(2)); h->next->next = UniquePtr<Link>(new Link(3)); h = std::move(h->next);', call: 'h->v * 10 + Link::live', expect: 22, compare: 'equal' }];
s2.widget.how = rep(s2.widget.how, 'Two compile checks fail if copying is allowed.', 'Two compile checks fail if copying is allowed. One test runs `h = std::move(h->next)` on a hidden list, where the source lives inside the object `h` lets go.');
s2.hints[2].text = rep(s2.hints[2].text, '`reset(p)` deletes the old one, then owns `p`.', '`reset(p)` owns `p` first, then deletes the old one.');
s2.explain.text = rep(s2.explain.text, 'The move hands it over and nulls the source, so exactly one destructor frees the object.', 'The move takes the source\'s pointer, then nulls the source before it deletes the old object, which may own it. So exactly one destructor frees each object.');

/* ---- CP5-1: l23 screens[4], the copy-assignment order ---- */
const s4 = L.screens[4];
const byId = (id) => s4.widget.lines.find(l => l.id === id);
byId('s1').text = 'copy `other`\'s `ptr_` and `count_` into locals, and add one to that count';
byId('s3').text = 'set `ptr_` and `count_` from the locals';
s4.hints[2].text = 'Read `other` into locals and add to its count, subtract from yourself, then set your pointers.';
s4.feedback.correct = 'Take the new share first, drop the old one second, set the pointers last: `a = a` stays safe.';
s4.explain.text = 'Adding first means `a = a` never lets the count reach zero. Reading `other` before the drop matters when the old object owns `other`, as in `head = head->next`: the drop destroys it. Dropping first could free the object you are about to share.';

/* ---- CP5-1: l23 screens[5] SharedPtr copy and move assignment ---- */
const s5 = L.screens[5];
const C_OLD = `    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            if (other.count_) ++*other.count_;
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
        }
        return *this;
    }`;
const C_NEW = `    SharedPtr& operator=(const SharedPtr& other) {
        if (count_ != other.count_) {
            T* p = other.ptr_;      // read the source first: the old object may own it
            long* c = other.count_;
            if (c) ++*c;
            drop();
            ptr_ = p;
            count_ = c;
        }
        return *this;
    }`;
const M_OLD = `    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            drop();
            ptr_ = other.ptr_;
            count_ = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
        }
        return *this;
    }`;
const M_NEW = `    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            T* p = other.ptr_;      // take the source first: the old object may own it
            long* c = other.count_;
            other.ptr_ = nullptr;
            other.count_ = nullptr;
            drop();
            ptr_ = p;
            count_ = c;
        }
        return *this;
    }`;
const TODO_OLD = '// TODO: copy assignment: let go of the old object, share the new one\n';
const TODO_NEW = '// TODO: copy assignment: share the new object, then let go of the old one (it may own `other`)\n';
s5.widget.starter = rep(s5.widget.starter, TODO_OLD, TODO_NEW);
if (!OLD) s5.widget.solution = rep(rep(s5.widget.solution, C_OLD, C_NEW), M_OLD, M_NEW);
s5.widget.postlude = LINK('SharedPtr');
const t5 = s5.widget.tests;
s5.widget.tests = [t5[0], t5[1],
  { setup: 'long n = 0; { SharedPtr<Tracked> a(new Tracked(1)); { SharedPtr<Tracked> b = a; SharedPtr<Tracked> c = b; } n = a.use_count() * 10 + Tracked::live; }', call: 'n * 10 + Tracked::live', expect: 110, compare: 'equal' },
  t5[4], t5[5], t5[6],
  { setup: 'long n = 0; { SharedPtr<Tracked> a(new Tracked(1)); SharedPtr<Tracked> b = std::move(a); n = b.use_count() * 10 + a.use_count(); }', call: 'n * 10 + Tracked::live', expect: 100, compare: 'equal' },
  ...t5.slice(9),
  { setup: 'SharedPtr<Link> h(new Link(1)); h->next = SharedPtr<Link>(new Link(2)); h = h->next;', call: 'h->v * 100 + h.use_count() * 10 + Link::live', expect: 211, compare: 'equal' },
  { setup: 'SharedPtr<Link> h(new Link(1)); h->next = SharedPtr<Link>(new Link(2)); h = std::move(h->next);', call: 'h->v * 100 + h.use_count() * 10 + Link::live', expect: 211, compare: 'equal' }];
s5.widget.how = rep(s5.widget.how, '`leakCheck` also fails a test whose counter block is never freed.', '`leakCheck` also fails a test whose counter block is never freed. Two tests run `h = h->next` and `h = std::move(h->next)` on a hidden list, where the source lives inside the object `h` lets go.');
s5.hints[2].text = 'Copy assignment: read `other`\'s pointers into locals and add one to its count. Then release your own and set yours from the locals.';

/* ---- CP5-1: l23 screens[7], the move it describes ---- */
const s7 = L.screens[7];
s7.hints[0].text = rep(s7.hints[0].text, 'before it takes', 'once it has taken');
s7.hints[1].text = '`b` takes over `a`\'s share without adding, then subtracts one for its old share.';
s7.widget.accept = '1: b took a\'s share and let go of its own';
s7.explain.text = 'The move assignment takes `a`\'s pointers without adding to the count, and empties `a`. It then drops `b`\'s old share, so the count falls from 2 to 1.';
wr('l23-own-smart-pointer.json', L);

/* ---- CP5-2: review-5 r5-unique-move-assign ---- */
const R5 = rd('review-5.json');
const r5 = R5.items.find(i => i.id === 'r5-unique-move-assign');
r5.widget.lines = [
  { id: 's3', text: '`other.ptr_ = nullptr;`' },
  { id: 'd1', text: '`delete other.ptr_;`', why: r5.widget.lines.find(l => l.id === 'd1').why },
  { id: 's5', text: '`ptr_ = p;`' },
  { id: 's1', text: '`if (this != &other) {`' },
  { id: 's6', text: '`return *this;`' },
  { id: 's2', text: '`T* p = other.ptr_;`' },
  { id: 's4', text: '`delete ptr_;`' }];
r5.widget.answer = ['s1', 's2', 's3', 's4', 's5', 's6'];
r5.feedback.correct = 'Guard, take theirs, null theirs, free your own, keep theirs, return.';
r5.feedback.generic = 'Not quite right. Take the other pointer and null the source before you free your own object.';
r5.explain.text = 'Take the other pointer and null the source first: the object you free may own the source, as in `head = std::move(head->next)`. Then free your own object and keep the taken pointer. With the guard, `a = std::move(a)` does nothing at all.';
wr('review-5.json', R5);

/* ---- CP5-2: homework-5 h5-shared-move-assign; CP5-3: h5-sole-and-counted self-move ---- */
const H5 = rd('homework-5.json');
const h5 = H5.items.find(i => i.id === 'h5-shared-move-assign');
const d1 = h5.widget.lines.find(l => l.id === 'd1');
h5.widget.lines = [
  { id: 's3', text: 'empty the source: set its `ptr_` and `count_` to null' },
  { id: 'd2', text: 'add one to the count you took', why: 'A move hands the share over. Adding one leaves the count one too high, so the object is never freed.' },
  { id: 's4', text: 'drop own count: subtract one, and at zero delete the object and the counter' },
  { id: 's1', text: '`if (this != &other) {`' },
  d1,
  { id: 's2', text: 'copy `other`\'s `ptr_` and `count_` into locals' },
  { id: 's5', text: 'set own `ptr_` and `count_` from the locals' }];
h5.widget.answer = ['s1', 's2', 's3', 's4', 's5'];
h5.feedback.correct = 'Guard, take, empty, drop, keep: one owner, one count.';
h5.feedback.generic = 'Not quite right. Take the source\'s share and empty the source before you drop your own: your old object may own the source.';
h5.feedback.byKey.d2 = 'You added one. A move hands the share over, so the count stays as it was.';
h5.explain.text = 'A move transfers the share, so the count does not change for the new object. The source is emptied before you drop your own share, because the object you drop may own the source.';
h5.canvas.params.lines[1] = '    // five steps; the if closes after the last';
const sc = H5.items.find(i => i.id === 'h5-sole-and-counted');
if (!OLD) sc.widget.solution = rep(sc.widget.solution, `        T* old = ptr_;
        ptr_ = other.release();   // take the source first: the old object may own it
        delete old;`, `        T* taken = other.release();   // take the source first: the old object may own it
        T* old = ptr_;
        ptr_ = taken;
        delete old;`);
sc.widget.tests[2].setup += ' SolePtr<Quote>& r = b; b = std::move(r);';
sc.prose = rep(sc.prose, '- Every assignment works for `a = a`, and', '- Every assignment works for `a = a` (for a `SolePtr`, `a = std::move(a)`), and');
wr('homework-5.json', H5);
console.log('applied' + (OLD ? ' (old solutions kept)' : ''));
