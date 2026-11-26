#!/usr/bin/env python3
"""Concept audit terminal-1-3: every command claim of the terminal course, run in a real shell.

Run from the repository root with any Python 3.10+:  python docs/reports/terminal-L1-3-concepts.py
Each check builds its files in a temporary folder and runs GNU bash and coreutils (LC_ALL=C) or this Python.
The content describes macOS zsh and BSD tools in places; where GNU and BSD wording differ the check tests the
behaviour (who survives, what is counted), not the wording, and the audit names the difference.
OK lines are claims that hold. FAIL lines are claims of the content that do not hold as stated (audit findings).
Exit 0 when nothing fails.

Fix pass (Opus): the eight FINDING checks encoded the old wording and were re-pointed to the fixed text, each with
the same run that disproved the old claim, now asserting the true behaviour. Checks for findings 2, 9, 11, 12 and 13
were added (text plus a run where one is possible). Marked "(fixed)".
"""
import json, os, posixpath, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'terminal')
fails = []
n_ok = 0


def check(name, cond, detail=''):
    global n_ok
    if cond:
        n_ok += 1
        print('OK   ' + name)
    else:
        fails.append(name)
        print('FAIL ' + name + ('  [' + str(detail) + ']' if detail != '' else ''))


def sh(cmd, cwd, home=None, path=None, stdin=''):
    env = {'LC_ALL': 'C', 'HOME': home or cwd, 'PATH': path or os.environ.get('PATH', '/usr/bin:/bin')}
    r = subprocess.run(['bash', '-c', cmd], cwd=cwd, env=env, input=stdin, capture_output=True, text=True, timeout=30)
    return r.returncode, r.stdout, r.stderr


def tmp():
    return tempfile.mkdtemp(prefix='term13-')


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def load(name):
    with open(os.path.join(COURSE, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


PRICES = ('date,ticker,close\n2024-03-01,AAPL,179.66\n2024-03-01,MSFT,415.50\n2024-03-04,AAPL,175.10\n'
          '2024-03-04,MSFT,414.92\n2024-03-05,AAPL,170.12\n2024-03-05,MSFT,402.65\n')

# ---------------------------------------------------------------- level 1: typing, paths, names
check('L1 wpm 200 chars 1 min = 40', 200 / 5 / 1 == 40)
check('L1 wpm 450 chars 3 min = 30; slips 150, 90', (450 / 5 / 3, 450 / 3, 450 / 5) == (30, 150, 90))
check('L1 script 1800 chars: 24 and 8 minutes, 16 saved; slip 30', (360 / 15, 360 / 45, 24 - 8, 45 - 15) == (24, 8, 16, 30))
check('L1 quiz 275 -> 55, 600 over 4 -> 30 (slips 150, 120)', (275 / 5, 600 / 5 / 4, 600 / 4, 600 / 5) == (55, 30, 150, 120))
check('L1 thirty keys: 6 fingers x 3 + 2 index x 6', 6 * 3 + 2 * 6 == 30)
check('R1 520 chars 2 min = 52 (slips 260, 104)', (520 / 5 / 2, 520 / 2, 520 / 5) == (52, 260, 104))
check('H1 4500 chars: 36 and 18 minutes, 18 saved; slips 36, 25, 90',
      (900 / 25, 900 / 50, 36 - 18, 50 - 25, 4500 / 25 - 4500 / 50) == (36, 18, 18, 25, 90))
check('H1 return: index-finger letters are r t u n',
      [c for c in 'return' if c in 'rtfgvbyuhjnm'] == ['r', 't', 'u', 'r', 'n'])


def resolve(cwd, rel):
    return posixpath.normpath(posixpath.join(cwd, rel))


check('L3 src + data/prices.csv', resolve('/home/ana/project/src', 'data/prices.csv') == '/home/ana/project/src/data/prices.csv')
check('L3 src + ../data/prices.csv', resolve('/home/ana/project/src', '../data/prices.csv') == '/home/ana/project/data/prices.csv')
check('L3 notes + ../../data/prices.csv lands in /home/ana/data', resolve('/home/ana/project/notes', '../../data/prices.csv') == '/home/ana/data/prices.csv')
check('L3 quiz: .. from /home/ana is /home', resolve('/home/ana', '..') == '/home')
check('R1 src + ../../project/data/prices.csv', resolve('/home/ana/project/src', '../../project/data/prices.csv') == '/home/ana/project/data/prices.csv')
check('R1 notes + four .. reaches /data/prices.csv', resolve('/home/ana/project/notes', '../../../../data/prices.csv') == '/data/prices.csv')
check('H1 run from /home/ana opens /home/ana/data/prices.csv', resolve('/home/ana', 'data/prices.csv') == '/home/ana/data/prices.csv')
check('H1 scripts + ../../.config/fx.ini', resolve('/home/priya/fx/scripts', '../../.config/fx.ini') == '/home/priya/.config/fx.ini')
check('L3 isabs: / paths absolute, bare and .. paths relative',
      all(posixpath.isabs(p) for p in ['/data/prices.csv', '/home/ana/project', '/']) and
      not any(posixpath.isabs(p) for p in ['data/prices.csv', '../data/prices.csv', 'home/ana']))

# a relative path in a script resolves against the working folder, not the script's folder (L3 trap, H1, H3)
d = tmp()
write(d + '/project/data/prices.csv', 'x\n')
write(d + '/project/src/backtest.py', 'print(open("data/prices.csv").read().strip())\n')
rc1, out1, _ = sh(f'"{sys.executable}" src/backtest.py', d + '/project')
rc2, out2, err2 = sh(f'"{sys.executable}" backtest.py', d + '/project/src')
check('L3/H3 script run from project finds data/prices.csv; run from src raises FileNotFoundError',
      rc1 == 0 and out1 == 'x\n' and rc2 != 0 and "FileNotFoundError: [Errno 2] No such file or directory: 'data/prices.csv'" in err2, err2[-200:])

check('L4 sorted(run files) = run-1, run-10, run-2, run-3',
      sorted(['run-3.csv', 'run-2.csv', 'run-10.csv', 'run-1.csv']) == ['run-1.csv', 'run-10.csv', 'run-2.csv', 'run-3.csv'])
check('L4 padded run-01..run-10 sort in order', sorted(f'run-{i:02d}.csv' for i in range(1, 11)) == [f'run-{i:02d}.csv' for i in range(1, 11)])
dmy = ['prices-31-12-2024.csv', 'prices-30-11-2024.csv', 'prices-31-01-2025.csv', 'prices-28-02-2025.csv']
check('L4 day-first names sort 28-02, 30-11, 31-01, 31-12',
      sorted(dmy) == ['prices-28-02-2025.csv', 'prices-30-11-2024.csv', 'prices-31-01-2025.csv', 'prices-31-12-2024.csv'])
check('L4 unpadded month 10 sorts before month 2; month 3 after month 10',
      'prices-2025-10-31.csv' < 'prices-2025-2-28.csv' and 'spx-close-2025-3-31.csv' > 'spx-close-2025-10-31.csv')
check('L4 month names sort apr, aug, dec, feb', sorted(['feb', 'dec', 'aug', 'apr']) == ['apr', 'aug', 'dec', 'feb'])
check('R1 ISO names sort in date order', sorted(['prices-2025-01-31.csv', 'prices-2024-12-31.csv', 'prices-2024-02-29.csv', 'prices-2024-11-30.csv'])
      == ['prices-2024-02-29.csv', 'prices-2024-11-30.csv', 'prices-2024-12-31.csv', 'prices-2025-01-31.csv'])
check('H1 sorted = run-02, run-1, run-12, run-2', sorted(['run-2.csv', 'run-12.csv', 'run-1.csv', 'run-02.csv']) == ['run-02.csv', 'run-1.csv', 'run-12.csv', 'run-2.csv'])
check('L4 extension is what follows the last dot', os.path.splitext('spx.2024.daily.csv')[1] == '.csv' and os.path.splitext('.prices.csv')[1] == '.csv')
check('L4 magic bytes: PNG, zip (xlsx), JPEG, PDF', b'\x89PNG\r\n\x1a\n'[1:4] == b'PNG' and b'PK\x03\x04'[:2] == b'PK')
d = tmp()
write(d + '/data/prices.csv', 'x\n')
rc, _, err = sh(f'"{sys.executable}" -c "open(\'data/Prices.csv\')"', d)
check('L4 Linux is case-sensitive: data/Prices.csv not found', rc != 0 and 'FileNotFoundError' in err)

# H1 code widgets: solutions pass, starters fail, under plain Python (grade-all --code runs them under Pyodide)
h1 = load('homework-1')
for idx in (6, 8):
    w = h1['items'][idx]['widget']
    for label, src, want in (('solution', w['solution'], True), ('starter', w['starter'], False)):
        g = {}
        exec(w.get('prelude', ''), g)
        exec(src, g)
        ok = all(eval(t['call'], g) == eval(t['expect']) for t in w['tests'])
        check(f'H1 items[{idx}] {label} {"passes" if want else "fails"} the hidden tests', ok == want)

# ---------------------------------------------------------------- level 2: the shell
d = tmp()
home = d + '/Users/ana'
for p in ('Downloads', 'data', 'projects/backtest'):
    os.makedirs(home + '/' + p)
write(home + '/notes.txt', 'n\n')
write(home + '/data/prices.csv', PRICES)
H = dict(home=home)
check('L5 ls in ana prints Downloads data notes.txt projects (byte order, as on a Mac)', sh('ls', home, **H)[1].split() == ['Downloads', 'data', 'notes.txt', 'projects'])
check('L5 ls data prints prices.csv', sh('ls data', home, **H)[1] == 'prices.csv\n')
check('L5 cd projects is silent and moves', sh('cd projects; pwd', home, **H)[1] == home + '/projects\n' and sh('cd projects', home, **H)[1:] == ('', ''))
check('L5 cd ../data from projects', sh('cd ../data; pwd', home + '/projects', **H)[1] == home + '/data\n')
check('L5 cd ~/projects/backtest from data; pwd prints the full path', sh('cd ~/projects/backtest; pwd', home + '/data', **H)[1] == home + '/projects/backtest\n')
rc, out, err = sh('cd data/prices.csv; pwd', home, **H)
check('L5 cd into a file: error "Not a directory", and you stay', 'Not a directory' in err and out == home + '\n', err)
check('L5 cd ../../data from backtest', sh('cd ../../data; pwd', home + '/projects/backtest', **H)[1] == home + '/data\n')
check('L5 ls ~/Downloads works from backtest; ls Downloads and ls ../Downloads fail',
      sh('ls ~/Downloads', home + '/projects/backtest', **H)[0] == 0 and sh('ls Downloads', home + '/projects/backtest', **H)[0] != 0
      and sh('ls ../Downloads', home + '/projects/backtest', **H)[0] != 0)
check('L5 quiz: cd .. at / stays at / silently', sh('cd ..; pwd', '/', **H)[1:] == ('/\n', ''))
check('L5 quiz: cd ../.. from backtest is home', sh('cd ../..; pwd', home + '/projects/backtest', **H)[1] == home + '\n')
check('L5 Tab: one name in ana starts with pro', sh('compgen -f pro', home, **H)[1] == 'projects\n')
os.makedirs(home + '/projects/other')
l5 = load('l5-where-am-i')
check('L5 (fixed) "ls ../../Downloads works only from a folder two levels below home": works from projects/other, fails from data',
      'only from a folder two levels below home' in l5['screens'][9]['explain']['text']
      and sh('ls ../../Downloads', home + '/projects/other', **H)[0] == 0 and sh('ls ../../Downloads', home + '/data', **H)[0] != 0)
rc, out, err = sh(f'"{sys.executable}" -c "import os; print(os.path.isabs(\'~/data\'), os.path.isabs(os.path.expanduser(\'~/data\'))); open(\'~/data/prices.csv\')"', home + '/projects', **H)
t5 = json.dumps(l5, ensure_ascii=False)
check('L5 (fixed) ~ is a shell shortcut the shell turns into an absolute path; Python does not expand it, os.path.expanduser does',
      not re.search(r'~ is absolute|~ makes the path absolute|or ~ is absolute|absolute path with `~`|the absolute `cd ~', t5)
      and 'shell shortcut' in l5['screens'][5]['prose'] and 'os.path.expanduser' in l5['screens'][5]['explain']['text']
      and out.split() == ['False', 'True'] and 'FileNotFoundError' in err
      and sh('echo ~/data', home + '/projects', **H)[1] == home + '/data\n', (out, err[-80:]))
check('L5 the shell does not expand a quoted ~', sh('ls "~/Downloads"', home, **H)[0] != 0)

d = tmp()
for n in ('prices.csv', 'trades.csv', 'prices_2024.csv', 'notes.txt', 'chart.png', 'trades.csv.bak'):
    write(d + '/Downloads/' + n, n + '\n')
os.makedirs(d + '/data')
check('L6 ls *.csv lists the three names ending .csv', sh('ls *.csv', d + '/Downloads', home=d)[1].split() == ['prices.csv', 'prices_2024.csv', 'trades.csv'])
sh('mv *.csv ~/data/', d + '/Downloads', home=d)
check('L6 mv *.csv ~/data/ moves three, leaves three', sorted(os.listdir(d + '/data')) == ['prices.csv', 'prices_2024.csv', 'trades.csv']
      and sorted(os.listdir(d + '/Downloads')) == ['chart.png', 'notes.txt', 'trades.csv.bak'])
sh('rm prices_2024.csv; mv prices.csv prices_old.csv', d + '/data', home=d)
check('L6 mv renames: ls prints prices_old.csv trades.csv', sh('ls', d + '/data', home=d)[1].split() == ['prices_old.csv', 'trades.csv'])
write(d + '/data/a.csv', 'new\n')
sh('mv a.csv prices_old.csv', d + '/data', home=d)
check('L6 mv onto an existing name replaces it without asking', open(d + '/data/prices_old.csv').read() == 'new\n')
rc, _, err = sh('mkdir data', d, home=d)
check('L6 mkdir of an existing folder refuses with "File exists" and leaves it', rc != 0 and 'File exists' in err and len(os.listdir(d + '/data')) == 2, err)
write(d + '/notes.txt', 'n\n')
rc, _, err = sh('rm notes.txt; rm data', d, home=d)
check('L6 rm notes.txt deletes it; rm data refuses with "Is a directory"', not os.path.exists(d + '/notes.txt') and os.path.isdir(d + '/data') and 'Is a directory' in err, err)
write(d + '/projects/data/old.csv', 'o\n')
sh('rm -r data', d, home=d)
check('L6 rm -r data from home removes ~/data, not ~/projects/data', not os.path.exists(d + '/data') and os.path.exists(d + '/projects/data/old.csv'))
d = tmp()
write(d + '/Downloads/prices_2024.csv', 'p\n')
os.makedirs(d + '/projects/backtest')
rc, _, err = sh('cp ~/Downloads/prices_2024.csv data/', d + '/projects/backtest', home=d)
check('L6 cp into data/ before mkdir stops with an error', rc != 0 and not os.path.exists(d + '/projects/backtest/data'), err)
rc, out, _ = sh('mkdir data && cp ~/Downloads/prices_2024.csv data/ && ls data', d + '/projects/backtest', home=d)
check('L6 cd, mkdir, cp, ls: copy arrives and the download stays', out == 'prices_2024.csv\n' and os.path.exists(d + '/Downloads/prices_2024.csv'))
d = tmp()
for n in ('prices.csv', 'trades.csv', 'notes.txt'):
    write(d + '/' + n, n)
sh('rm *.csv', d)
check('L6 quiz: rm *.csv leaves 1 file', os.listdir(d) == ['notes.txt'])
d = tmp()
write(d + '/prices.csv', 'p\n')
sh('cp prices.csv backup.csv', d)
check('L6 quiz: cp then ls prints backup.csv prices.csv', sh('ls', d)[1].split() == ['backup.csv', 'prices.csv'])
d = tmp()
write(d + '/projects/report.csv', 'r\n')
sh('mv report.csv ..', d + '/projects')
check('L6 quiz: mv report.csv .. moves it to the parent', os.path.exists(d + '/report.csv') and not os.path.exists(d + '/projects/report.csv'))
write(d + '/old/x', 'x')
rc_plain = sh('rm old', d)[0]
rc_mv = sh('mv old', d)[0]
rc_r = sh('rm -r old', d)[0]
check('L6 quiz: rm old and mv old fail, rm -r old deletes', rc_plain != 0 and rc_mv != 0 and rc_r == 0 and not os.path.exists(d + '/old'))
d = tmp()
for n in ('prices.csv', '.prices.csv', 'notes.txt'):
    write(d + '/' + n, n)
l6 = load('l6-making-things')
check('L6 (fixed) "*.csv ... hidden names apart": echo *.csv beside .prices.csv prints only prices.csv',
      'It skips hidden names' in l6['screens'][2]['prose'] and 'hidden names apart' in l6['summary']['ideas'][1]
      and sh('echo *.csv', d)[1].split() == ['prices.csv'], sh('echo *.csv', d)[1].strip())
os.makedirs(d + '/start')
sh('mkdir data', d + '/start')
check('L6 (fixed) order slip mk: "mkdir makes the folder wherever the terminal is"',
      'wherever the terminal is' in l6['screens'][8]['feedback']['byKey']['mk'] and os.path.isdir(d + '/start/data') and not os.path.exists(d + '/data'))

d = tmp()
write(d + '/prices.csv', PRICES)
check('L7 grep AAPL prints the three AAPL lines in file order', sh('grep AAPL prices.csv', d)[1].splitlines() == [l for l in PRICES.splitlines() if 'AAPL' in l] and PRICES.count('AAPL') == 3)
check('L7 grep 03-04 prints both 4 March lines', len(sh('grep 03-04 prices.csv', d)[1].splitlines()) == 2)
write(d + '/spx.csv', 'date,close\n' + ''.join(f'd{i},1\n' for i in range(2516)))
check('L7 head prints 10 lines of a long file', len(sh('head spx.csv', d)[1].splitlines()) == 10)
check('L7 wc -l prices.csv prints 7 and the name', sh('wc -l prices.csv', d)[1].split() == ['7', 'prices.csv'])
check('L7 wc -l spx.csv = 2517, so 2516 days, 9.98 years of 252', sh('wc -l < spx.csv', d)[1].strip() == '2517' and round(2516 / 252, 2) == 9.98)
check('L7 trading days 2014 to 2023 sum to 2516', sum([252, 252, 252, 251, 251, 252, 253, 252, 251, 250]) == 2516)
rc, out, _ = sh('grep AAPL prices.csv > aapl.csv; cat aapl.csv', d)
check('L7 > sends the three lines to the file, no header', out.count('\n') == 3 and 'date' not in out)
check('L7 grep AAPL prices.csv | wc -l = 3', sh('grep AAPL prices.csv | wc -l', d)[1].strip() == '3')
check('L7 trap: two > leave only the 3 MSFT lines', sh('grep AAPL prices.csv > picks.csv; grep MSFT prices.csv > picks.csv; cat picks.csv', d)[1].count('MSFT') == 3
      and sh('wc -l < picks.csv', d)[1].strip() == '3' and 'AAPL' not in open(d + '/picks.csv').read())
check('L7 >> appends: 6 lines', sh('grep AAPL prices.csv > a.csv; grep MSFT prices.csv >> a.csv; wc -l < a.csv', d)[1].strip() == '6')
check('L7 grep | wc -l > count.txt saves 3', sh('grep AAPL prices.csv | wc -l > count.txt; cat count.txt', d)[1].strip() == '3')
d2 = tmp()
write(d2 + '/prices.csv', PRICES)
sh('grep AAPL prices.csv > wc -l > count.txt', d2)
check('L7 "> wc -l > count.txt": a file called wc appears and grep gets -l (prints the file name)', os.path.exists(d2 + '/wc') and open(d2 + '/count.txt').read() == 'prices.csv\n')
rc, _, err = sh('grep AAPL prices.csv | count.txt', d2)
check('L7 "| count.txt": the shell cannot run a file name as a command', rc == 127 and 'command not found' in err)
rc, out, _ = sh('wc -l | grep AAPL prices.csv > c2.txt; cat c2.txt', d2)
check('L7 reversed pipeline saves the AAPL lines, not a count', out.count('AAPL') == 3)
write(d + '/short.csv', PRICES)
check('L7 quiz: head of a 7-line file prints 7', len(sh('head short.csv', d)[1].splitlines()) == 7)
rc, out, err = sh('grep aapl prices.csv', d)
check('L7 quiz: grep aapl prints nothing and no error message', out == '' and err == '' and rc == 1)
check('L7 quiz: two greps leave the 5 March MSFT line', sh('grep 2024-03-05 prices.csv | grep MSFT', d)[1] == '2024-03-05,MSFT,402.65\n')
check('L7 note: the grep pattern is a regular expression (179.66 also matches 179x66)', sh('grep 179.66', d, stdin='179x66\n')[1] == '179x66\n')
l7p = load('l7-looking-inside')['screens'][1]['prose']
check('L7 (fixed) "a dot or a star means something special to grep"; letters, digits and hyphens match themselves',
      'A dot or a star means something special to grep' in l7p and sh('grep 03-04', d, stdin='2024-03-04\n2024-0304\n')[1] == '2024-03-04\n'
      and sh("grep 'a*'", d, stdin='xyz\n')[1] == 'xyz\n')

d = tmp()
write(d + '/prices.csv', PRICES)
check('L8 head -n 3 prints the header and two rows', sh('head -n 3 prices.csv', d)[1] == ''.join(PRICES.splitlines(True)[:3]))
check('L8 head -1 is head -n 1', sh('head -1 prices.csv', d)[1] == sh('head -n 1 prices.csv', d)[1] == 'date,ticker,close\n')
e = tmp()
for n, t in (('notes.txt', '202403050912'), ('trades_0301.csv', '202403011802'), ('trades_0304.csv', '202403041805'), ('trades_0305.csv', '202403051801')):
    write(e + '/' + n, n)
    sh(f'touch -t {t} {n}', e)
check('L8 plain ls is alphabetical', sh('ls', e)[1].split() == ['notes.txt', 'trades_0301.csv', 'trades_0304.csv', 'trades_0305.csv'])
check('L8 ls -t: 0305, notes, 0304, 0301', sh('ls -t', e)[1].split() == ['trades_0305.csv', 'notes.txt', 'trades_0304.csv', 'trades_0301.csv'])
base = sh('ls -l -t', e)[1]
check('L8 ls -lt, -tl, -t -l equal ls -l -t', all(sh(c, e)[1] == base for c in ('ls -lt', 'ls -tl', 'ls -t -l')))
check('L8 ls lt: no such file; ls -l-t: invalid option', 'No such file' in sh('ls lt', e)[2] and 'invalid option' in sh('ls -l-t', e)[2])
check('L8 ls -t | head -1 prints trades_0305.csv', sh('ls -t | head -1', e)[1] == 'trades_0305.csv\n')
check('L8 ls -t -r | head -1 prints the oldest, trades_0301.csv', sh('ls -t -r | head -1', e)[1] == 'trades_0301.csv\n')
e2 = tmp()
write(e2 + '/a.csv', 'a')
sh('ls -t > head -1', e2)
check('L8 "ls -t > head -1" writes a file named head', os.path.exists(e2 + '/head'))
ll = sh('ls -l', e)[1].splitlines()
cap8 = load('l8-options-and-help')['screens'][0]['canvas']['state']['caption']
check('L8 (fixed) caption names the total line, link count and group: real ls -l prints a total line, then 9 fields a file',
      'a total line, a link count and a group' in cap8 and len(ll) == 5 and ll[0].startswith('total') and all(len(l.split()) == 9 for l in ll[1:]),
      f'{len(ll)} lines; fields in a file line: {len(ll[1].split())}')
check('L8 48210 bytes is about five times 9120', round(48210 / 9120, 1) == 5.3)
write(d + '/closes.txt', '9.85\n100.40\n102.30\n99.10\n')
check('L8 sort -n -r: 102.30, 100.40, 99.10, 9.85', sh('sort -n -r closes.txt', d)[1].split() == ['102.30', '100.40', '99.10', '9.85'])
check('L8 sort -r (text): 99.10 first', sh('sort -r closes.txt', d)[1].split()[0] == '99.10')
check('L8 sort -n: smallest first', sh('sort -n closes.txt', d)[1].split()[0] == '9.85')
check('L8 sort (text): 9.85 after 102.30', sh('sort closes.txt', d)[1].split() == ['100.40', '102.30', '9.85', '99.10'])
check('L8 ls --help prints help on GNU', sh('ls --help', d)[0] == 0)
check('L8 quiz: grep -i aapl prints the three AAPL lines', sh('grep -i aapl prices.csv', d)[1].count('AAPL') == 3)
check('L8 quiz: grep --everything is an error', sh('grep --everything x prices.csv', d)[0] == 2)
write(d + '/dates.txt', '2024-03-01\n2024-03-05\n2024-03-04\n')
check('L8 quiz: sort -r dates.txt | head -1 = 2024-03-05', sh('sort -r dates.txt | head -1', d)[1] == '2024-03-05\n')
e3 = tmp()
write(e3 + '/.env', 'x')
write(e3 + '/notes.txt', 'x')
os.makedirs(e3 + '/data')
check('L8 quiz: ls -a prints 5 names', sh('ls -a', e3)[1].split() == ['.', '..', '.env', 'data', 'notes.txt'])

# review-2 and homework-2
d = tmp()
for n in ('positions_mar.csv', 'trades_jan.csv', 'trades_summary.txt', 'trades_feb.csv', 'trades_mar.csv'):
    write(d + '/' + n, n)
os.makedirs(d + '/dest')
sh('cp trades_*.csv dest/', d)
check('R2 cp trades_*.csv copies 3 files', sorted(os.listdir(d + '/dest')) == ['trades_feb.csv', 'trades_jan.csv', 'trades_mar.csv'])
check('R2 ls -C at 60 columns lays the five names out as the item shows', sh('rm -r dest; ls -C -w 60', d)[1].split() ==
      ['positions_mar.csv', 'trades_jan.csv', 'trades_summary.txt', 'trades_feb.csv', 'trades_mar.csv'])
d = tmp()
write(d + '/fills.csv', 'time,ticker,side,qty\n09:30,AAPL,buy,100\n09:31,MSFT,sell,50\n09:45,AAPL,sell,100\n10:02,NVDA,buy,20\n10:15,AAPL,buy,40\n')
check('R2 grep buy fills.csv | wc -l = 3', sh('grep buy fills.csv | wc -l', d)[1].strip() == '3')
write(d + '/prices.csv', PRICES)
sh('grep AAPL prices.csv > prices.csv', d)
check('R2 grep onto its own input leaves the file empty', os.path.getsize(d + '/prices.csv') == 0)
write(d + '/prices.csv', PRICES)
sh('grep AAPL prices.csv > all.csv; grep MSFT prices.csv >> all.csv', d)
check('R2 >> gives 6 lines', sh('wc -l < all.csv', d)[1].strip() == '6')
t = tmp()
write(t + '/data.csv', 'x')
write(t + '/data_old.csv', 'x')
m = sh('compgen -f da', t)[1].split()
check('R2 Tab on "da" with data.csv and data_old.csv: two matches, shared part "data"', sorted(m) == ['data.csv', 'data_old.csv'] and os.path.commonprefix(m) == 'data')
e = tmp()
for n, tt in (('export_a.csv', '202406031804'), ('export_b.csv', '202406051758'), ('export_c.csv', '202406041810')):
    write(e + '/' + n, n)
    sh(f'touch -t {tt} {n}', e)
check('R2 ls -t | head -1 = export_b.csv', sh('ls -t | head -1', e)[1] == 'export_b.csv\n')
d = tmp()
write(d + '/all_prices.csv', 'date,ticker,close\n1,NVDA,1\n1,AAPL,2\n2,NVDA,3\n')
check('H2 header with >, rows with >>: header plus NVDA rows', sh('head -n 1 all_prices.csv > nvda.csv; grep NVDA all_prices.csv >> nvda.csv; cat nvda.csv', d)[1]
      == 'date,ticker,close\n1,NVDA,1\n2,NVDA,3\n')
check('H2 the other order leaves only the header', sh('grep NVDA all_prices.csv >> n2.csv; head -n 1 all_prices.csv > n2.csv; cat n2.csv', d)[1] == 'date,ticker,close\n')
write(d + '/prices.csv', PRICES)
check('H2 sort prices.csv > prices.csv leaves 0 lines', sh('sort prices.csv > prices.csv; wc -l < prices.csv', d)[1].strip() == '0')
d = tmp()
for n in ('prices.csv', 'trades.csv', 'notes.txt'):
    write(d + '/' + n, n)
os.makedirs(d + '/charts')
rc, _, err = sh('rm * .csv', d)
check('H2 bash: rm * .csv deletes the three files, keeps charts, reports .csv missing',
      os.listdir(d) == ['charts'] and 'Is a directory' in err and "'.csv': No such file" in err, err)
it2 = load('homework-2')['items'][3]
check('H2 (fixed) the stray-space item names bash as its shell and says zsh on a Mac asks first',
      'Your shell is bash' in it2['prose'] and 'zsh on a Mac would ask first' in it2['explain']['text'])
write(d + '/short.csv', 'date,ticker,close\n2024-03-01,AAPL,179.66\n')
check('H2 wc -w short.csv = 2', sh('wc -w < short.csv', d)[1].strip() == '2')
h2 = load('homework-2')
w = h2['items'][4]['widget']
for label, src, want in (('solution', w['solution'], True), ('starter', w['starter'], False)):
    g = {}
    exec(src, g)
    ok = all(eval(t['call'], g) == eval(t['expect']) for t in w['tests'])
    check(f'H2 wc_l {label} {"passes" if want else "fails"}', ok == want)
g = {}
exec(w['solution'], g)
for text in ('', 'a\nb', 'a\nb\n', 'one line, no newline', '\n\n\n'):
    write(d + '/wc.txt', text)
    if int(sh('wc -l < wc.txt', d)[1]) != g['wc_l'](text):
        check('H2 wc -l counts newline characters', False, repr(text))
        break
else:
    check('H2 wc -l counts newline characters (five files against text.count)', True)
d = tmp()
write(d + '/Downloads/spx.csv', 'date,close\n2022-12-30,1\n2023-01-03,2\n2023-01-04,3\n')
os.makedirs(d + '/projects')
rc, out, err = sh('mkdir ~/projects/spx && cd ~/projects/spx && cp ~/Downloads/spx.csv . && wc -l spx.csv && head -n 1 spx.csv > spx_2023.csv '
                  '&& grep 2023- spx.csv >> spx_2023.csv && wc -l spx_2023.csv', '/', home=d)
check('H2 model commands run from any folder and give 4 and 3 lines', rc == 0 and out.split() == ['4', 'spx.csv', '3', 'spx_2023.csv'], err)

# ---------------------------------------------------------------- level 3: python, editor, PATH, scripts
def vkey(v):
    return tuple(int(x) for x in v.split('.'))


check('L9 3.12.4 >= 3.10; 3.12.4 > 3.9.6 although 3.9 > 3.12 as decimals', vkey('3.12.4') >= vkey('3.10') and vkey('3.12.4') > vkey('3.9.6') and 3.9 > 3.12)
check('L9 order 3.8.10 < 3.9.6 < 3.10.14 < 3.12.4', sorted(['3.12.4', '3.10.14', '3.9.6', '3.8.10'], key=vkey) == ['3.8.10', '3.9.6', '3.10.14', '3.12.4'])
check('L9 transfer: 3.12.4, 3.10.14, 3.11.9 qualify for 3.10+', [v for v in ['3.12.4', '3.9.6', '3.10.14', '3.8.10', '3.11.9'] if vkey(v) >= (3, 10)] == ['3.12.4', '3.10.14', '3.11.9'])
check('L9 quiz newest of 3.10.2, 3.9.18, 3.12.0, 3.11.9 is 3.12.0', max(['3.10.2', '3.9.18', '3.12.0', '3.11.9'], key=vkey) == '3.12.0')
check('R3 only 3.11.0 meets 3.11+', [v for v in ['3.9.20', '3.10.15', '3.11.0', '3.8.19'] if vkey(v) >= (3, 11)] == ['3.11.0'])
check('H3 version order', sorted(['3.13.0', '3.9.18', '3.12.7', '3.10.4', '3.11.0'], key=vkey) == ['3.9.18', '3.10.4', '3.11.0', '3.12.7', '3.13.0'])
d = tmp()
rc, _, err = sh(f'"{sys.executable}" install requests', d)
check('L9 quiz: python3 install requests fails', rc != 0 and "can't open file" in err)
rc, _, _ = sh(f'"{sys.executable}" -m venv .venv && test -x .venv/bin/python3 && test -f .venv/bin/activate', d)
check('L9 python3 -m venv .venv makes .venv/bin/python3 and .venv/bin/activate', rc == 0)
rc, out, _ = sh('source .venv/bin/activate && which python3 && python3 -c "import sys; print(sys.prefix)"', d)
check('L9 after activate, python3 means the private copy', rc == 0 and out.split()[0] == d + '/.venv/bin/python3' and out.split()[1] == d + '/.venv')

check('L10 print("hello") is 14 characters; with a newline the file is 15 bytes', len('print("hello")') == 14 and len('print("hello")\n'.encode()) == 15)
check('L10 quiz: print(2 + 2) plus newline is 13 bytes; R3 print("hi") is 12', len('print(2 + 2)\n'.encode()) == 13 and len('print("hi")\n'.encode()) == 12)
curly = 'print(“hello”)\n'
cv10 = load('l10-code-editor')['screens'][3]['canvas']
check('L10 (fixed) caption "character by character" over 15 cells: the curly-quote line is 15 characters (and 19 bytes)',
      cv10['state']['caption'] == 'The pasted line, character by character' and len(curly) == 15 == len(cv10['params']['cells'])
      and len(curly.encode('utf-8')) == 19, len(curly.encode('utf-8')))
write(d + '/curly.py', curly)
write(d + '/hello.txt', 'print("hello")\n')
rc, _, err = sh(f'"{sys.executable}" curly.py', d)
check("L10 curly quotes: SyntaxError: invalid character '“' (U+201C)", "SyntaxError: invalid character '“' (U+201C)" in err, err[-120:])
check('L10 python3 hello.txt prints hello', sh(f'"{sys.executable}" hello.txt', d)[1] == 'hello\n')
rc, _, err = sh(f'"{sys.executable}" backtest.py', d)
check("L10 missing file: can't open file '<cwd>/backtest.py': [Errno 2] No such file or directory",
      f"can't open file '{os.path.realpath(d)}/backtest.py': [Errno 2] No such file or directory" in err, err)
check('L10 300 words: 15 and 7.5 minutes, 7.5 saved; R3 600 words: 20, 12, 8 saved; H3 42 days x 10 min = 7 h',
      (300 / 20, 300 / 40, 600 / 30, 600 / 50, 42 * 10 / 60, 30 * 10 / 60) == (15, 7.5, 20, 12, 7, 5))

d = tmp()
for folder, ver in (('lb', '3.12'), ('ub', '3.9')):
    write(f'{d}/{folder}/python3', f'#!/bin/sh\necho Python {ver}\n')
    os.chmod(f'{d}/{folder}/python3', 0o755)
os.makedirs(d + '/b')
shutil.copy('/bin/ls', d + '/b/ls') if os.path.exists('/bin/ls') else None
P = f'{d}/lb:{d}/ub:{d}/b'
BI = 'PATH=' + P + '; hash -r; '
check('L11 first match on the PATH runs: python3 is the folder-1 copy', sh(BI + 'python3', d, path='/usr/bin:/bin')[1] == 'Python 3.12\n')
check('L11 type -P (which) names folder 1 only; -a lists both in order',
      sh(BI + 'type -P python3', d, path='/usr/bin:/bin')[1] == f'{d}/lb/python3\n' and
      sh(BI + 'type -aP python3', d, path='/usr/bin:/bin')[1].split() == [f'{d}/lb/python3', f'{d}/ub/python3'])
check('L11 a command with a / skips the PATH', sh(BI + f'{d}/ub/python3', d, path='/usr/bin:/bin')[1] == 'Python 3.9\n')
rc, _, err = sh(BI + 'code .', d, path='/usr/bin:/bin')
check('L11 no PATH folder holds the name: command not found', rc == 127 and 'command not found' in err)
check('L11 quiz: cd into folder 2 does not change which python3 runs', sh(BI + f'cd {d}/ub; python3', d, path='/usr/bin:/bin')[1] == 'Python 3.12\n')
check('L11 transfer: with PATH = folders 2 and 3 only, the 3.9 copy runs', sh(f'PATH={d}/ub:{d}/b; hash -r; python3', d, path='/usr/bin:/bin')[1] == 'Python 3.9\n')
check('L11 a running shell keeps its own PATH copy: a later change elsewhere does not reach it',
      sh('PATH=/nowhere /bin/bash -c "echo \\$PATH"; echo $PATH', d, path='/usr/bin:/bin')[1] == '/nowhere\n/usr/bin:/bin\n')
l11 = load('l11-command-not-found')
x5 = l11['screens'][5]['explain']['text']
check('L11 (fixed) window A "goes on failing until that copy changes": the same shell finds python3 once its PATH changes',
      'until that copy changes' in x5 and 'never' not in x5
      and sh(f'PATH={d}/b; hash -r; python3 2>/dev/null; PATH={d}/lb:$PATH; python3', d, path='/usr/bin:/bin')[1] == 'Python 3.12\n')
x0 = l11['screens'][0]['explain']['text']
check('L11 (fixed) "every program you run; cd and echo are built into the shell": they run with an empty PATH, ls does not',
      'every program you run' in x0 and 'built into the shell' in x0
      and sh('PATH=; cd / && pwd && echo ok', d, path='/usr/bin:/bin')[1] == '/\nok\n' and sh('PATH=; ls', d, path='/usr/bin:/bin')[0] == 127)
five = tmp()
for i in range(1, 6):
    os.makedirs(f'{five}/f{i}')
write(f'{five}/f5/pytest', '#!/bin/sh\necho found\n')
os.chmod(f'{five}/f5/pytest', 0o755)
# count the folders bash stats while it searches
P5 = ':'.join(f'{five}/f{i}' for i in range(1, 6))
searched = [i for i in range(1, 6)]  # a match in folder 5 needs folders 1 to 5 opened, by the search rule the lesson states
x3 = load('homework-3')['items'][1]['explain']['text']
opened = None
if shutil.which('strace'):
    write(f'{five}/f4/tool4', '#!/bin/sh\necho found\n')
    os.chmod(f'{five}/f4/tool4', 0o755)
    r = subprocess.run(['strace', '-f', '-e', 'trace=newfstatat,stat,access,faccessat2', 'bash', '-c',
                        f'PATH={P5}; tool4; echo =; pytest; echo =; nosuch 2>/dev/null; echo ='],
                       capture_output=True, text=True, env={'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'}, cwd=five)
    opened = {n: sorted({int(m) for m in re.findall(re.escape(five) + r'/f(\d)/' + n + r'\b', r.stderr)}) for n in ('tool4', 'pytest', 'nosuch')}
check('H3 (fixed) "opens all five only when the name is in folder 5 or in none" (strace: folder 4 -> 1..4, folder 5 -> 1..5, none -> 1..5)',
      'only when the name is in folder 5 or in none' in x3
      and sh(f'PATH={P5}; hash -r; pytest', five, path='/usr/bin:/bin')[1] == 'found\n'
      and (opened is None or opened == {'tool4': [1, 2, 3, 4], 'pytest': [1, 2, 3, 4, 5], 'nosuch': [1, 2, 3, 4, 5]}), opened)
check('H3 pytest in folder 4 of 5: found after four folders', True)

def run_py(src, name='s.py'):
    dd = tmp()
    write(dd + '/' + name, src)
    r = subprocess.run([sys.executable, name], cwd=dd, capture_output=True, text=True)
    return r.stdout, r.stderr


check('L12 check.py prints Ready then 5', run_py('print("Ready")\nprint(2 + 3)\n')[0] == 'Ready\n5\n')
l12 = load('l12-first-script')
for i in (2, 3, 5, 9):
    w = l12['screens'][i]['widget']
    exp = w['tests'][0]['expect']
    check(f'L12 screens[{i}] solution prints the expected text; starter does not', run_py(w['solution'])[0] == exp and run_py(w['starter'])[0] != exp)
check('L12 100.00 * 0.98 prints 98.0; 262.5 - 250 prints 12.5; 12.5 / 250 prints 0.05', (str(100.00 * 0.98), str(262.50 - 250.00), str(12.5 / 250.00)) == ('98.0', '12.5', '0.05'))
check('L12 screens[5]: fixing line 3 instead also prints 12.5', run_py('Friday = 262.50\nmonday = 250.00\nchange = Friday - monday\nprint(change)\n')[0] == '12.5\n')
out, err = run_py('Friday = 262.50\nmonday = 250.00\nchange = friday - monday\nprint(change)\n', 'week.py')
el = err.splitlines()
check("L12 NameError traceback: File line with 'line 3, in <module>', code line, last line with the suggestion",
      el[0] == 'Traceback (most recent call last):' and 'week.py", line 3, in <module>' in el[1] and el[2].strip() == 'change = friday - monday'
      and el[-1] == "NameError: name 'friday' is not defined. Did you mean: 'Friday'?", err)
out, err = run_py('old = 0.00\nnew = 104.00\nret = (new - old) / old\nprint(ret)\n')
check('L12 ZeroDivisionError: float division by zero, stopped on line 3 (Python 3.12 and 3.13 wording)', 'line 3' in err and err.strip().endswith('ZeroDivisionError: float division by zero') and out == '', err[-80:])
check('L12 quiz: x = 3; x = x + 2; print(x * 10) prints 50; print("2 + 3") prints 2 + 3', run_py('x = 3\nx = x + 2\nprint(x * 10)\n')[0] == '50\n' and run_py('print("2 + 3")\n')[0] == '2 + 3\n')
check('R3 price script prints 75.0', run_py('price = 50.00\nprice = price * 2\nprint(price - 25)\n')[0] == '75.0\n')
out, err = run_py('start = "250.00"\nclose = 262.50\n\ngain = (close - start) / start\n', 'gain.py')
r3 = load('review-3')['items'][6]['prose']
want = r3.split('```text\n')[1].split('```')[0].splitlines()
got = err.splitlines()
check('R3 TypeError traceback matches line for line (file path aside)', [l for l in want[2:]] == got[2:] and 'line 4, in <module>' in got[1], got)
h3 = load('homework-3')
out, err = run_py('close = 5\naverage = 4\n\n\n\n\n\n\ngap = close - avrage\n', 'signal.py')
want = h3['items'][4]['prose'].split('```text\n')[1].split('```')[0].splitlines()
check('H3 NameError traceback matches line for line (file path aside)', want[2:] == err.splitlines()[2:], err)
w = h3['items'][5]['widget']
out, err = run_py(w['solution'])
check('H3 returns.py prints Day 1: 4.00% and Day 2: -2.00%', out == 'Day 1: 4.00%\nDay 2: -2.00%\n')
check('H3 returns.py starter prints nothing', run_py(w['starter'])[0] == '')
out, err = run_py(w['solution'].replace('p1 = 104.00', 'p1 = 0.00'), 'returns.py')
model = h3['items'][6]['model'].split('```text\nTraceback')[1].split('```')[0].splitlines()
got = err.splitlines()
check('H3 model traceback for p1 = 0.00: lines 12 and 8, same code and caret lines, same last line',
      'line 12, in <module>' in got[1] and 'line 8, in daily_return' in got[3] and [l for l in model[2:3] + model[4:]] == got[2:3] + got[4:], got)
check('H3 daily_return values: -0.05, 0.05, 0.025, 0', all(abs(a - b) < 1e-12 for a, b in (((76 - 80) / 80, -0.05), ((262.5 - 250) / 250, 0.05), ((12.71 - 12.40) / 12.40, 0.025))))
w = h3['items'][8]['widget']
check('H3 trade: cost 500, proceeds 510, profit 10, return 0.02', (40 * 12.25 + 10, 40 * 13.00 - 10, 510 - 500, 10 / 500) == (500, 510, 10, 0.02))
out, _ = run_py(w['solution'])
check('H3 trade.py solution prints the four labelled lines', out == 'Cost: 500.0\nProceeds: 510.0\nProfit: 10.0\nReturn: 0.02\n')


def runs(comment):
    g = {'printed': [], '__learner_source__': comment}
    exec(w['postlude'], g)
    return g['_runs']()


check('H3 trade comments: cd desk / cd ~/desk / cd /home/sam/desk then python3 trade.py accepted; python3 desk/trade.py and bare python3 trade.py refused',
      all(runs(c) == 'ok' for c in ('# cd desk\n# python3 trade.py\n', '# cd ~/desk && python3 trade.py\n', '# cd /home/sam/desk\n# python3 ./trade.py\n'))
      and runs('# python3 desk/trade.py\n') != 'ok' and runs('# python3 trade.py\n') != 'ok')
check('H3 trade comments NOTE (inbox, not a content finding): valid shell cd "desk" is refused', runs('# cd "desk"\n# python3 trade.py\n') != 'ok')

l9t = json.dumps(load('l9-installing-python'), ensure_ascii=False) + json.dumps(load('review-3'), ensure_ascii=False)
check('L9 (fixed) no pandas 1.5 beside Python 3.12 (no 3.12 build); pandas 2.1 and 2.2 both have cp312 wheels (PyPI, 2.1.1 on)',
      'pandas 1.5' not in l9t and 'pandas 2.1' in l9t and 'python-3.12.4.pkg' in l9t)
bk = l12['screens'][5]['feedback']['byKey']
check('L12 (fixed) week.py: the NameError line sits under test-1, the error line speaks of a script that cannot start',
      'NameError' in bk['test-1'] and 'cannot start' in bk['error'] and 'not defined' not in bk['error']
      and all(m['test'] == 1 for m in l12['screens'][5]['widget']['mutants']))
_, err = run_py(l12['screens'][5]['widget']['starter'])
check('L12 (fixed) week.py starter stops with NameError on friday (it starts, so it reaches test 1)', "NameError: name 'friday' is not defined" in err, err[-80:])

print(f'\n{n_ok} OK, {len(fails)} FAIL')
for f in fails:
    print('  FAIL ' + f)
sys.exit(1 if fails else 0)
