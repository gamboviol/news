"""
convert documents from SMART format to simple line of words
"""

import sys
import os

if len(sys.argv) != 3:
    print 'Usage: {0} smart_file low_file'.format(sys.argv[0])
    raise SystemExit(1)

infile = open(sys.argv[1])
lowfile = sys.argv[2]

docfile = open(lowfile+'.docs','wb')
doc = None
count = 0
for line in infile:
    line = line.strip()
    if not line and doc is not None:
        print >>docfile,doc
        count += 1
        doc = None
    elif doc is None:
        doc = line.split()[1]
    elif line == '.W':
        continue
    else:
        doc += ' '+line
infile.close()
docfile.close()

countfile = open(lowfile+'.count','wb')
print >>countfile,count
countfile.close()

os.system('cat {0}.count {0}.docs > {0}'.format(lowfile))
os.system('rm {0}.count {0}.docs'.format(lowfile))
