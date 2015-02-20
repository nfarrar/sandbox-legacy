=========
Debugging
=========


Notes
=====
- Use set -v to enable verbose output (prints lines as they are read to stderr, before substitutions and expansions are applied)
- Use set -x to enable xtrace (prints lines to stderr as they are executed, after substitutions and expansions are applied)

Echo to stderr
--------------
Using a simple echo::

    echo "DEBUG: current i=$i" >&2

Basic xtrace
------------
Running the entire script in debug mode::

    bash -x bash-boilerplate.sh

Targeted xtrace
---------------
To debug specific parts of the script, use set -x (enabled) and set +x (disable) debugging for those sections::

    set +x
        # [code to debug ...]
    set -x

Formatting xtrace
-----------------
PS4 contains the formatting to be applied to xtrace output, we can include additional information by configuring this prompt::

    export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'


Using a Debug Flag
------------------
We can use a simple flag & function to enable and disable debugging::

    # enable debugging
    F_DEBUG=1

    debug() {
        [[ $F_DEBUG = 1 ]] && "$@" || :
    }

    debug set -x
    # [code to debug ...]
    debug set +x

    debug logger "Sorting the database"
    database_sort
    debug logger "Finished sorting the database, exit code $?"


Resources
=========

Tools
-----
- `BASH Debugger                                                <http://bashdb.sourceforge.net/>`_

Guides
------
- `Debugging Bash Scripts                                       <http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_02_03.html>`_
- `Debugging with the BASH debugger                             <http://bashdb.sourceforge.net/bashdb.html>`_
- `Bash\-Hacker's Wiki \- Debugging a script                    <http://wiki.bash-hackers.org/scripting/debuggingtips>`_
