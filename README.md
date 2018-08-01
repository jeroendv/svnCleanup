[![Build Status](https://travis-ci.com/jeroendv/svnCleanup.svg?branch=master)](https://travis-ci.com/jeroendv/svnCleanup)

[![Coverage Status](https://coveralls.io/repos/github/jeroendv/svnCleanup/badge.svg?branch=master)](https://coveralls.io/github/jeroendv/svnCleanup?branch=master)

# svnCleanup

Free disk space by recursive finding all svn working copies in the current folder and clean them.

E.g.
```
for all svn wc in current dir tree:
    cd <svn wc>
    svn cleanup
```
will not change the working copy in any way!

in addition it will also write a log of the original and new .svn folder size and how much spaces was freed.

# usage

```
$ python svncleanup.py  -h
usage: svncleanup.py [-h] [path]

Recursively invode 'svn cleanup' on all svn WC in a directory tree. Appending
info to `svncleanup.log`


positional arguments:
  path        dir tree root path (defaults to cwd)

optional arguments:
  -h, --help  show this help message and exit

```

e.g. `$ python svncleanup.py <path to dir tree root>` will do the trick

```
$ python svncleanup.py  <projectPath>
Dir Tree Root: <projectPath>
2018-07-30 14:45:40.103632
241.1Mb  -> 200.0Mb  = 41.1Mb     .\.svn
592.1Mb  -> 592.1Mb  = 0.0b     .\Packages\boost\.svn

total freed space: 41.1Mb

```

alternatively 

1) copy the script to the folder that needs to be cleaned() e.g. local dev folder containing all your svn project checkouts for example)
1) run the script, e.g. double click it
1) check the 'svncleanup.log' file to see what you gained ;-)





# refs
http://svnbook.red-bean.com/en/1.6/svn.ref.svn.c.cleanup.html
