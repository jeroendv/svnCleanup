
"""Find all svn working copies in the current folder and clean them.

This can potentially free up a lot of disk space.

http://svnbook.red-bean.com/en/1.6/svn.ref.svn.c.cleanup.html
"""
import os
from os.path import*
import subprocess
import datetime
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="""Recursively invode 'svn cleanup' on all svn WC in a directory tree.
    Appending info to `svncleanup.log`""",)

    parser.add_argument('path'
                    , help="dir tree root path (defaults to cwd)"
                    , nargs="?"
                    , default=".")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # verify is path points to directory
    if not os.path.isdir(args.path):
        print("folder does not exists: "+args.path)
        sys.exit(-1)

    # excaption safety
    originalDir = os.getcwd()
    try:
        os.chdir(args.path)
        print("Dir Tree Root: "+ os.getcwd())
        CleanDirTree()
    finally:
        os.chdir(originalDir)


def CleanDirTree():
    Log(str(datetime.datetime.now()))

    svnRepoSizes = []
    ignoredFolders = ['.svn', '.git']
    for (root, dirs, files) in os.walk('.'):
        # perform cleanup for each svn checkout
        if '.svn' in dirs:
            svnDir = os.path.join(root,'.svn')

            byteSize_before = dir_size(svnDir)
            cleanSvnWcRepo(root)
            byteSize_after = dir_size(svnDir)

            svnRepoSizes.append(SvnRepoSize(svnDir, byteSize_before, byteSize_after))

        # don't walk into ignored folders
        for d in ignoredFolders:
            if d in dirs:
                dirs.remove(d)

    ## sort the data and print in order of freed up space
    for e in sorted(svnRepoSizes, key=SvnRepoSize.size_difference):
        Log("{:8} -> {:8} = {:8} {}".format(
            humanReadableSize(e.bytes_before),
            humanReadableSize(e.bytes_after),
            humanReadableSize(e.size_difference()),
            e.path
        ))

    ## log the total freed space as well
    totalSize_before = 0+ sum([e.bytes_before for e in svnRepoSizes])
    totalSize_after = 0+ sum([e.bytes_after for e in svnRepoSizes])
    totalFreedSpaceInBytes = 0 + sum([e.size_difference() for e in svnRepoSizes])

    Log("{:8} -> {:8} = {:8} {}".format(
            humanReadableSize(totalSize_before),
            humanReadableSize(totalSize_after),
            humanReadableSize(totalFreedSpaceInBytes),
            "TOTAL"
        ))
    Log("")

class SvnRepoSize:
    """track size of a .svn folder before and after the svn cleanup"""
    def __init__(self, path, bytes_before, bytes_after):
        self.path = path
        self.bytes_before = bytes_before
        self.bytes_after = bytes_after

    def size_difference(self):
        return self.bytes_after - self.bytes_before

def Log(str):
    """write `str` to both stdout and append it to a file"""
    with open('svnCleanup.log', 'at') as f:
        f.write(str + "\n")

    print(str)

class DirSizeError(Exception): pass


def dir_size(start, follow_links=0, skip_errs=0):
    """compute a folder size in bytes
    
    https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch04s24.html
    """

    # Get a list of all names of files and subdirectories in directory start
    try: dir_list = os.listdir(start)
    except:
        # If start is a directory, we probably have permission problems
        if os.path.isdir(start):
            raise DirSizeError('Cannot list directory %s'%start)
        else:  # otherwise, just re-raise the error so that it propagates
            raise

    total = 0
    for item in dir_list:
        # Get statistics on each item--file and subdirectory--of start
        path = join(start, item)
        try: stats = os.stat(path)
        except: 
            if not skip_errs:
                raise DirSizeError('Cannot stat %s'%path)
        # The size in bytes is in the seventh item of the stats tuple, so:
        total += stats[6]
        # recursive descent if warranted
        if isdir(path) and (follow_links or not islink(path)):
            bytes = dir_size(path, follow_links)
            total += bytes
    return total

def humanReadableSize(byteSize):
    """Return human readable size string e.g. Gb, Mb, Kb, b """
    if abs(byteSize) >= 1024**3:
        return '{:.1f}Gb'.format(byteSize / 1024 / 1024 / 1024)
    elif abs(byteSize) >= 1024**2:
        return '{:.1f}Mb'.format(byteSize / 1024 / 1024 )
    elif abs(byteSize) >= 1024:
        return '{:.1f}Kb'.format(byteSize / 1024  )
    else:
        return '{:.1f}b'.format(byteSize)


def cleanSvnWcRepo(svnWC):
    """clean the svn WC Repo
    """
    assert os.path.isdir(svnWC)
    pwd = os.getcwd()
    try:
        os.chdir(svnWC)
        exitcode = 0
        try:
            cmd = ['svn', 'cleanup', '--vacuum-pristines']
            subprocess.check_output(cmd) 
            return 
        except subprocess.CalledProcessError as e:
            exitcode = e.returncode
            
        # fallback to regular cleanup if call failed
        assert exitcode != 0
        try:
            cmd = ['svn', 'cleanup']
            subprocess.check_output(cmd)
            return
        except subprocess.CalledProcessError as e:
            Log("svn cleanup failed : " + svnWC)          
            raise e
    finally:
        # always go back to original working directory
        os.chdir(pwd)





if __name__ == '__main__':
    main()


    



       

