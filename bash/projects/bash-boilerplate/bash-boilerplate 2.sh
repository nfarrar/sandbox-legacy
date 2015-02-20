#!/usr/bin/env bash
# @Author:             Nathan Farrar
# @Date:               2014-08-31 10:50:29
# @Last Modified by:   Nathan Farrar
# @Last Modified time: 2014-08-31 12:18:55

#/ Usage: ./bash-boilerplate.sh
#/   Bash Boilerplate - A Framework for Building Bash Scripts
#/   Copyright (C) 2014  Nathan Farrar
#/   This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#/   This is free software, and you are welcome to redistribute it
#/   under certain conditions; type `show c' for details.


# Strict Execution
# ----------------
set -o nounset                          # generate an error if we attempt to modify an unset variable
set -o pipefail                         # preserve pipeline errors
set -o errexit                          # exit when errors are generated
set -o noclobber                        # do not overwrite files
shopt -s extglob                        # enable extended globbing (required for pattern matching)
shopt -s extdebug                       # enable extended debugging (required for function stack trace)
IFS=$'\n\t'                             # do not use spaces as a field separator


# Generic Exit Codes
# ------------------
E_SUCCESS=0                             # exit code for successful execution
E_ERR_UNKNOWN=1                         # exit code for an unknown error

E_ERR_FUNCTION_ARGS=10                  # exit code for when a function is called with the wrong arguments
E_ERR_NOT_IMPLIMENTED=11                # exit code when an unimplemented function is called


die() {
    local $error_code = $@

    cleanup
    return $error_code
}

cleanup() {
    message "Performing cleanup" $C_DEBUG
}


# [150] Messages
# --------------
C_DEBUG=0                                   # debugging messages    (CLI: --debug)
C_INFO=1                                    # info messages         (CLI: --verbose)
C_WARN=2                                    # warning messages
C_ERROR=3                                   # error messages
C_DEBUG_COLOR=$C_FG_MAGENTA                 # the color to use when writing DEBUG messages to console
C_INFO_COLOR=$C_FG_GREEN                    # the color to use when writing INFO messages to console
C_WARN_COLOR=$C_FG_YELLOW                   # the color to use when writing WARN messages to console
C_ERROR_COLOR=$C_FG_RED                     # the color to use when writing ERROR messages to console

F_MSG_LEVEL=$C_DEBUG                        # the lowest message level to display (messages below this level will be discarded)
F_MSG_LEVEL_DEFAULT=$C_DEBUG                # the default message level to use when message is called without an argument
F_MSG_CONSOLE=1                             # write messages to console (STDOUT, STDERR)
F_MSG_LOGFILE=0                             # write messages to our logfile ()
F_MSG_SYSLOG=0                              # send messages to syslog

S_LOG_FILE='boilerplate.log'                # write logs to this file (if F_MSG_LOGFILE=1)
S_DATE_PATTERN='+%Y/%m/%d:%H:%M:%S'         # the date pattern to use when writting messages

message() {
    local $msg="$1"
    local $level="$2"

    if [ $F_MSG_CONSOLE == 1 ]; then
        message_write_console $msg $level
    fi

    if [ $FMSG_LOGFILE == 1 ]; then
        message_write_logfile $msg $level
    fi

    if [ $F_MSG_SYSLOG == 1 ]; then
        message_write_syslog $msg $level
    fi
}

message_write_console() {
    message "$FUNCNAME not implemented."
    die $E_ERR_NOT_IMPLIMENTED
}

message_write_logfile() {
    message "$FUNCNAME not implemented."
    die $E_ERR_NOT_IMPLIMENTED
}

message_write_syslog() {
    message "$FUNCNAME not implemented."
    die $E_ERR_NOT_IMPLIMENTED
}









