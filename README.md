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

1) copy the script to the folder that needs to be cleaned() e.g. local dev folder containing all your svn project checkouts for example)
1) run the script
1) check the 'svncleanup.log' file to see what you gained ;-)


# refs
http://svnbook.red-bean.com/en/1.6/svn.ref.svn.c.cleanup.html