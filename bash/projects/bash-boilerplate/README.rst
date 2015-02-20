================
bash-boilerplate
================

.. image:: https://badge.fury.io/gh/nfarrar%2Fbash-boilerplate.svg
    :target: http://badge.fury.io/gh/nfarrar%2Fbash-boilerplate

.. image:: https://travis-ci.org/nfarrar/bash-boilerplate.png?branch=master
        :target: https://travis-ci.org/nfarrar/bash-boilerplate


About
-----
I'm so tired of rewriting the same code over and over for my bash scripts.

The boilerplate consists of self-contained modules, written for
inter-module compatibility.

The bash-boilerplate.sh script uses its own modules to build new scripts::

    # download & install the supplementary libraries to ~/.local/lib
    ./bash-boilerplate.sh --init

    # list the available modules
    ./bash-boilerplate.sh --list-modules

    # build a new script using the listed modules
    ./bash-boilerplate.sh --build <name> --modules debug,traps,cli-options\
        cfg-file,req-user=root

Features
--------

* TODO: Drop it like it's hot.

License
-------
Bash Boilerplate - A Framework for Building Bash Scripts
Copyright (C) 2014  Nathan Farrar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
