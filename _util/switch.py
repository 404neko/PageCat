import os
import sys
import shutil

if __name__=='__main__':
    if len(sys.argv)!=3:
        print 'ERROR'
        exit()
    file = sys.argv[1]
    which = sys.argv[2]
    if os.path.isfile('..'+os.sep+'_config'+os.sep+file+'.py'):
        os.remove('..'+os.sep+'_config'+os.sep+file+'.py')
    if os.path.isfile('..'+os.sep+'_config'+os.sep+file+os.sep+which+'.py'):
        shutil.copy('..'+os.sep+'_config'+os.sep+file+os.sep+which+'.py','..'+os.sep+'_config'+os.sep+file+'.py')
        os.system('cat '+'..'+os.sep+'_config'+os.sep+file+'.py')
    else:
        print 'FAIl'