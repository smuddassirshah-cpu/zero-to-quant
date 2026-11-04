// node codecheck.mjs : every Python code widget of research-int level 4 and its drills, in Pyodide: solution passes all tests and examples, starter fails.
import fs from 'fs'; import path from 'path'; import {createRequire} from 'module';
const root='/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/pkgs/pyodide-0.27.7/package/';
const W='/home/user/zero-to-quant/.claude/worktrees/agent-a8859a2b6006bfb36/app/';
const files=['l16-interpolating','l17-regression-by-group','l18-updating-a-fit','l19-timed-data-task','l20-writing-a-take-home','review-4','homework-4'];
const drills=['rq-interp-py','rq-group-slopes-py','rq-online-ols-py','rq-clean-frame-py'];
const widgets=[];
function walk(o, where){ if(Array.isArray(o)){o.forEach((x,i)=>walk(x,where+'/'+i));return;} if(o&&typeof o==='object'){ if(o.kind==='code'&&(o.language||'python')==='python') widgets.push({where,w:o}); for(const k of Object.keys(o)) walk(o[k],where+'/'+k);} }
for(const f of files){ walk(JSON.parse(fs.readFileSync(W+'content/courses/research-int/'+f+'.json','utf8')), f); }
for(const d of drills){ widgets.push({where:'drill '+d, w:JSON.parse(fs.readFileSync(W+'content/drills/'+d+'.json','utf8'))}); }
const only=process.argv[2];
const require=createRequire(root);
const {loadPyodide}=require(root+'pyodide.js');
const py=await loadPyodide({indexURL:root, stdout:()=>{}, stderr:()=>{}});
await py.loadPackage(['numpy','pandas','scipy','scikit-learn','statsmodels']);
const runner=`
import json, math, os, shutil, traceback, time
def cmp(compare, actual, expect, tol):
    def tl(v):
        if hasattr(v,'tolist'): return v.tolist()
        return v
    a, e = tl(actual), expect
    if compare == 'equal':
        return a == e
    def one(x, y):
        if isinstance(x,(list,tuple)) or isinstance(y,(list,tuple)):
            return len(x)==len(y) and all(one(p,q) for p,q in zip(x,y))
        t = tol or {}
        rel = t.get('rel', 1e-9 if not t else 0); ab = t.get('abs', 1e-12 if not t else 0)
        return math.isclose(float(x), float(y), rel_tol=rel, abs_tol=ab)
    return one(a, e)
def run_widget(spec, source):
    ns = {'__name__': '__main__'}
    res = []
    try:
        if spec.get('prelude'): exec(spec['prelude'], ns)
        ns['__learner_source__'] = source
        exec(source, ns)
        if spec.get('postlude'): exec(spec['postlude'], ns)
    except Exception as ex:
        return [('load', False, repr(ex)[:200])]
    for i, t in enumerate(spec['tests']):
        t0 = time.time()
        try:
            if t.get('setup'): exec(t['setup'], ns)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); res.append((i, False, 'no error'))
                except Exception as ex:
                    names = [c.__name__ for c in type(ex).__mro__]
                    res.append((i, t['expect'] in names, '' if t['expect'] in names else 'raised ' + repr(ex)[:100]))
                continue
            actual = eval(t['call'], ns); expect = eval(t['expect'], ns)
            ok = cmp(t.get('compare','isclose'), actual, expect, t.get('tol'))
            res.append((i, bool(ok), ('' if ok else 'got %r expected %r' % (actual, expect))[:300] + ' [%.2fs]' % (time.time()-t0)))
        except Exception as ex:
            res.append((i, False, 'error ' + repr(ex)[:150]))
    return res
`;
py.runPython(runner);
let bad=0;
for(const {where,w} of widgets){
  if(only && !where.includes(only)) continue;
  for(const f of Object.keys(w.data||{})){ py.FS.writeFile('/home/pyodide/'+f, fs.readFileSync(W+w.data[f])); }
  py.FS.chdir('/home/pyodide');
  const spec=JSON.stringify({prelude:w.prelude||'',tests:w.tests});
  const t0=Date.now();
  py.globals.set('SPEC_JSON', spec); py.globals.set('SOL', w.solution); py.globals.set('STA', w.starter);
  const out=py.runPython(`
import json
spec=json.loads(SPEC_JSON)
r1=run_widget(spec, SOL)
r2=run_widget(spec, STA)
spec2=dict(spec); spec2['tests']=json.loads(json.dumps(${JSON.stringify(w.examples||[])}))
r3=run_widget(spec2, SOL) if spec2['tests'] else []
json.dumps({'sol':r1,'sta':r2,'ex':r3})
`);
  const r=JSON.parse(out);
  const solFail=r.sol.filter(x=>!x[1]), exFail=r.ex.filter(x=>!x[1]), staPass=r.sta.filter(x=>x[1]);
  const staAllPass = staPass.length===r.sta.length;
  console.log(`${where}: solution ${r.sol.length-solFail.length}/${r.sol.length}, examples ${r.ex.length-exFail.length}/${r.ex.length}, starter passes ${staPass.length}/${r.sta.length} (${((Date.now()-t0)/1000).toFixed(1)} s)`);
  for(const x of solFail) console.log('   SOLUTION FAIL', JSON.stringify(x));
  for(const x of exFail) console.log('   EXAMPLE FAIL', JSON.stringify(x));
  if(staPass.length) console.log('   starter passes', JSON.stringify(staPass.map(x=>x[0])));
  if(solFail.length||exFail.length||staAllPass||staPass.length>1) { bad++; }
  if(process.argv[3]==='times') console.log('   ', r.sol.map(x=>x[2].slice(-9)).join(' '));
}
console.log(bad?`PROBLEMS ${bad}`:'ALL CODE OK');
