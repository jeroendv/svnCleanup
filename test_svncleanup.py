import os

import svncleanup
import sys

def test(tmpdir):
    tmpdir = str(tmpdir)
    print("tmpdir: " + tmpdir)
    print("tmpdir is dir :" + str(os.path.isdir(tmpdir)))
    print("pwd: " + os.getcwd())


def test_svnclenaupModuleInvocation(tmpdir):
    tmpdir = str(tmpdir)
    os.chdir(tmpdir)

    # set cli arg and invode script main
    # which should not raise
    sys.argv = [svncleanup.__name__]
    svncleanup.main()

    # verify that log file is created
    assert os.path.isfile('svnCleanup.log')

