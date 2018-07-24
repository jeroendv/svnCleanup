
"""Find all svn working copies in the current folder and clean them.

This can potentially free up a lot of disk space.

http://svnbook.red-bean.com/en/1.6/svn.ref.svn.c.cleanup.html
"""
import os
from os.path import*
import subprocess
import datetime

def main():

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
        dirs = filter(lambda e: e not in ignoredFolders, dirs)

    ## sort the data and print in order of freed up space
    sortedTable = sorted(svnRepoSizes, key=SvnRepoSize.size_difference)
    for e in sortedTable:
        totalFreedSpaceInBytes += e.size_difference
        Log("{:8} -> {:8} = {:8} {}".format(
            humanReadableSize(e.bytes_before),
            humanReadableSize(e.bytes_after),
            humanReadableSize(e.size_difference),
            e.path
        ))

    ## log the total freed space as well
    totalFreedSpaceInBytes = sum([e.size_difference() for e in svnRepoSizes])
    Log("total freed space: {}".format(humanReadableSize(totalFreedSpaceInBytes)))
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
    if byteSize >= 1024**3:
        return '{:.1f}Gb'.format(byteSize / 1024 / 1024 / 1024)
    elif byteSize >= 1024**2:
        return '{:.1f}Mb'.format(byteSize / 1024 / 1024 )
    elif byteSize >= 1024:
        return '{:.1f}Kb'.format(byteSize / 1024  )
    else:
        return '{:.1f}b'.format(byteSize)


def cleanSvnWcRepo(svnWC):
    """clean the svn WC Repo
    """
    pwd = os.getcwd()
    try:
        # print("$ cd "+svnWC, flush=True)
        os.chdir(svnWC)

        cmd = ['svn', 'cleanup']
        # print("$ "+" ".join(cmd), flush=True)
        # subprocess.check_call(cmd) 


    finally:
        os.chdir(pwd)




if __name__ == '__main__':
    main()


    



       

