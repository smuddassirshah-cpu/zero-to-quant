import json,glob,os,sys
base='/home/user/zero-to-quant/.claude/worktrees/agent-a6c7287c786a6bcf6/app/content/courses/'
for c in ['ito','measure-prob','pdes']:
    tot=0
    for f in sorted(glob.glob(base+c+'/l*.json'), key=lambda x:int(os.path.basename(x).split('-')[0][1:])):
        d=json.load(open(f))
        tot+=d['minutes']
        print(c,d['id'][:28].ljust(28),d['minutes'],d['skills'],'|',' / '.join(i[:100] for i in d['summary']['ideas'][:3]))
    print('total min',tot)
