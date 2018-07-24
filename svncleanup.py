
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

    byteSizes_before = []
    byteSizes_after = []
    paths = []
    ignoreFolders = ['.svn', '.git']
    for (root, dirs, files) in os.walk('.'):
        # perform cleanup for each svn checkout
        if '.svn' in dirs:
            svnDir = os.path.join(root,'.svn')

            byteSizes_before.append(dir_size(svnDir))

            cleanSvnWcRepo(root)

            byteSizes_after.append(dir_size(svnDir))
            paths.append(svnDir)

        # don't walk into ignored folders
        for f in ignoreFolders:
            if (f in dirs):
                dirs.remove(f) 

    ## sort the data and print in order of freed up space
    table = zip(byteSizes_before, byteSizes_after, paths)
    sortedTable = sorted(table, key=lambda e: e[1]-e[0])
    totalFreedSpaceInBytes = 0
    for (b,a,p) in sortedTable:
        sizeDiffBytes = a-b
        totalFreedSpaceInBytes += sizeDiffBytes
        Log("{:8} -> {:8} = {:8} {}".format(
            humanReadableSize(b),
            humanReadableSize(a),
            humanReadableSize(sizeDiffBytes),
            p
        ))
    Log("total freed space: {}".format(humanReadableSize(totalFreedSpaceInBytes)))
    Log("")

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


    



       

