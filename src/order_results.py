import sys
import os
import os.path
import subprocess

scores={}

for root, dirs, files in os.walk(sys.argv[2]):
    for dir in dirs:
        for root_, dirs_, files_ in os.walk(root+'/'+dir):
            for file in files_:
                if file.endswith('.txt') or file.endswith('.dump'):
                    sp = subprocess.check_output(['octave','--path','src/octave/',
                'src/octave/pan14_author_verification_eval.m','-i',
                root_+'/'+file,'-t',sys.argv[1],'-o','/dev/null'])

                    scores[root_+'/'+file]={}
                    for line in sp.splitlines():
                        if line.startswith('SP') or line.startswith('EE') or line.startswith('EN'):
                            bits=line.split()
                            for bit in bits:
                                if '=' in bit:
                                    bits_=bit.split('=')
                                    scores[root_+'/'+file][bits_[0]]=bits_[1]


aucs=[(float(v['AUC']),k) for k,v in scores.iteritems()]
aucs.sort()
c1s=[(float(v['C@1']),k) for k,v in scores.iteritems()]
c1s.sort()
res=[(float(v['AUC'])*(float(v['C@1'])),k) for k,v in scores.iteritems()]
res.sort()

print 'AUC',aucs
print 'C@1',c1s
print 'final',res

