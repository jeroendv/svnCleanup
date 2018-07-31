import os

def test(tmpdir):
    print(tmpdir)
    print(os.path.isdir(tmpdir))

