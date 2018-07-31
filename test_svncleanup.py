import os

import svncleanup
import sys
import subprocess

def test(tmpdir):
    tmpdir = str(tmpdir)
    print("tmpdir: " + tmpdir)
    print("tmpdir is dir :" + str(os.path.isdir(tmpdir)))
    print("pwd: " + os.getcwd())


def test_svncleanupModuleInvocation(tmpdir):
    tmpdir = str(tmpdir)
    os.chdir(tmpdir)

    # set cli arg and invode script main
    # which should not raise
    sys.argv = [svncleanup.__name__]
    svncleanup.main()

    # verify that log file is created
    assert os.path.isfile('svnCleanup.log')
    # there should be 2 lines  in the log
    # header time line & totals line & empty newline
    f = open('svnCleanup.log','rt')
    lines = f.readlines()
    assert 3 == len(lines)
    
    assert lines[-1] == '\n'

def test_svncleanupModuleInvocation2(tmpdir):
    tmpdir = str(tmpdir)
    os.chdir(tmpdir)

    # create an svn repo and check it out
    subprocess.check_call('svnadmin create svnRepo', shell=True)
    subprocess.check_call('svn checkout file://{}/svnRepo svnWc'.format(tmpdir), shell=True)

    # set cli arg and invode script main
    # which should not raise
    sys.argv = [svncleanup.__name__]
    svncleanup.main()

    # verify that log file is created
    assert os.path.isfile('svnCleanup.log')

    # there should be 3 lines  in the log
    # header time line, a single line for ./svnWc/ & totals line & empty newline
    f = open('svnCleanup.log','rt')
    lines = f.readlines()
    assert 4 == len(lines)
    assert lines[-1] == '\n'

