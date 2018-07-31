import os

import svncleanup
import sys

def test(tmpdir):
    print("tmpdir: " + str(tmpdir))
    print("tmpdir is dir :" + str(os.path.isdir(tmpdir)))
    print("pwd: " + os.getcwd())


def test_svnclenaupModuleInvocation(tmpdir):
    os.chdir(tmpdir)

    # set cli arg and invode script main
    # which should not raise
    sys.argv = [svncleanup.__name__]
    svncleanup.main()

    # verify that log file is created
    assert os.path.isfile('svnCleanup.log')

