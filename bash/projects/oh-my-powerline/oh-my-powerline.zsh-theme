# @Author:  Nathan Farrar
# @Email:   nathan.farrar@gmail.com
# @Website: http://crunk.io/


# TODO: Replace oh-my-zsh plugins with native code.
# TODO: Add support for PS4 & debugging prompt.


# ZSH Settings
# ------------
# Enable zsh color bindings.
autoload -U colors && colors

# Enable hooks (chpwd, periodic, precmd, preexec, zshaddhistory, zshexit).
#   precmd  - Executed before each prompt.
#   preexec - Executed just after a command has been read and is about to be executed.
autoload -U add-zsh-hook

# Enable command substitutions & parameter expansions.
setopt prompt_subst


# Globals
# -------
# NOTE: Why does using declare to define the integer values break them?

declare -A SYMBOLS
declare -a SEGMENTS

PROMPT_ID=0
SEG_COUNT=0
CURRENT_BG=''

USERNAME=''
HOSTNAME=''
HISTLINE=0
JOBCOUNT=0
RETVAL=0
TERMWIDTH=0


# Unicode Symbols
# ---------------

SYMBOLS[BRANCH]=''
SYMBOLS[LINE]=''
SYMBOLS[PADLOCK]=''
SYMBOLS[LSEP]=''
SYMBOLS[LSEP_ALT]=''
SYMBOLS[RSEP]=''
SYMBOLS[RSEP_ALT]=''

SYMBOLS[SMILE]='☺'
SYMBOLS[FROWN]='☹'
SYMBOLS[VENV]='λ'

SYMBOLS[APPLE]=''
SYMBOLS[FLAG]='⚑'
SYMBOLS[DOT]='✹'
SYMBOLS[YINGYANG]='☯'
SYMBOLS[BIOHAZARD]='☢'
SYMBOLS[STAR]='★'
SYMBOLS[CHECK]='✔'
SYMBOLS[XMARK]='✘'
SYMBOLS[FILE]='⨍'

SYMBOLS[SPADE]='♠'
SYMBOLS[CLUB]='♣'
SYMBOLS[HEARTS]='❤'
SYMBOLS[DIAMOND]='♦'

SYMBOLS[ALEFT]='←'
SYMBOLS[AUP]='↑'
SYMBOLS[ARIGHT]='→'
SYMBOLS[ADOWN]='↓'

SYMBOLS[CMD]='⌘'
SYMBOLS[OPT]='⌥' 
SYMBOLS[CTRL]='⌃' 
SYMBOLS[SHIFT]='⇧' 
SYMBOLS[CAPSLOCK]='⇪' 
SYMBOLS[TAB]='⇥' 
SYMBOLS[TABSHIFT]='⇤' 
SYMBOLS[RETURN]='↩' 
SYMBOLS[ENTER]='⌤' 
SYMBOLS[DEL]='⌫' 
SYMBOLS[DELFOR]='⌦' 
SYMBOLS[PUP]='⇞' 
SYMBOLS[PDOWN]='⇟' 
SYMBOLS[HOME]='↖' 
SYMBOLS[END]='↘' 
SYMBOLS[CLEAR]='⌧' 
SYMBOLS[SPACE]='␣' 
SYMBOLS[POWER]='⎋' 
SYMBOLS[EJECT]='⏏'

SYMBOLS[GIT]='Ⓖ'
SYMBOLS[MERCURIAL]='Ⓜ'
SYMBOLS[SVN]='Ⓢ'
SYMBOLS[CVS]='Ⓒ'
SYMBOLS[BZR]='Ⓑ'
SYMBOLS[VCS]='Ⓥ'


# Settings
# --------
DEBUG=1
LSEP=$SYMBOLS[LSEP]
RSEP=$SYMBOLS[RSEP]


# Debug Messages
# --------------
# Display debugging messages if enabled. Set DEBUG=1 to enable them.

function debug() {
    [[ $DEBUG == 1 ]] && echo "DEBUG: $1" 1>&2;
}


# OMPL Precmd
# -----------
# Commands to be executed prior to building the prompt.
# Immediately set the return value of the last executed command.

function precmd() {
    RETVAL=$?
    (( TERMWIDTH = ${COLUMNS} - 1 ))
}
add-zsh-hook precmd precmd


# Test Segment
# ------------
# Generate a simple segment for testing purposes.
# The colors module stores the color bindings in an indexed array, therefore
# we can select a random color using: $((RANDOM % 8)).

function segment_test() {
    [ -n "$1" ] && fgc=$1 || fgc=$(shuf -i 1-7 -n 1)
    add_segment $(shuf -i 1000-9999 -n 1) $fgc 'black'
}


# Error Segment
# -------------
# If the previous command failed, the return status is displayed in a red 'error' segment.
# $RETVAL is set immediately in ompl_precmd (prior to the prompt being built).
function segment_error() {
    if [[ $RETVAL -ne 0 ]]; then
        add_segment "$RETVAL" 'red' 'black'
    fi
}


# Context Segment
# ---------------
# If we're using a local session, add the username & hostname to the context
# segment. If we're in a remote session, add the username, ip & port.

function segment_context() {
    local user=`whoami`

    if [[ -z "$SSH_CLIENT" ]]; then
        add_segment "%n@%m" 'yellow' 'black'
    else
        local ip=$(echo $SSH_CLIENT | cut -f1 -d ' ')
        local port=$(echo $SSH_CLIENT | cut -f3 -d ' ')

        add_segment "%n@$ip:$port" 'yellow' 'black'
    fi
}


# Path Segment
# ------------
# Display the current path.

function segment_path() {
    add_segment "%~" 'blue' 'black'
}


# Version Control Segment
# -----------------------
# TODO: Add version control segment features.

function segment_vc() {

}


# ZSH_THEME_GIT_PROMPT_CLEAN=$OMPL_SYMBOL_CHECK
# ZSH_THEME_GIT_PROMPT_DIRTY=$OMPL_SYMBOL_X
# ZSH_THEME_GIT_PROMPT_PREFIX="$OMPL_SYMBOL_POWERLINE_VERSION_CONTROL_BRANCH "
# ZSH_THEME_GIT_PROMPT_SUFFIX=" "
# function ompl_segment_git() {
#     build_segment "$(git_prompt_info)" 'cyan' 'black'
# }


# Timestamp Segment
# -----------------
# Add a timestamp segment.
# TODO: Move pattern to config section.

function segment_timestamp() {
    # add_segment 'timestamp' 'magenta' 'black'
    add_segment '%D{%Y-%m-%d %H:%M:%S}' 'magenta' 'black'
}


# Virtualenv Segment
# ------------------
# TODO: Add virtualenv segment.

# Requires the virtualenv plugin by Tony Seek. To install with antigen add the
# following line to your .zshrc:
# bundle antigen bundle tonyseek/oh-my-zsh-virtualenv-prompt
# export ZSH_THEME_VIRTUAL_ENV_PROMPT_PREFIX=$OMPL_SYMBOL_FILE
# export ZSH_THEME_VIRTUAL_ENV_PROMPT_SUFFIX=" "

# function _segment_virtualenv() {
#     if [[ -n $VIRTUAL_ENV ]]; then
#         build_segment "$(virtualenv_prompt_info)" 'magenta' 'black'
#     fi
# }


# Add Segment
# -----------
# Adds a newline delimited string containing the commands to be executed with
# the corresponding bg & fg colors to the segments array. This allows for more
# much clearer segment drawing than the method utilized in the agnoster (and
# other powerline clone) themes. Segment content cannot contain newlines.

function add_segment() {
    local segment="$(echo -en "$1;$2;$3")"
    local index=${#SEGMENTS[@]}

    SEGMENTS+=$segment
}


# Draw Segments
# -------------
# Draw the segments in the $SEGMENT array.

function draw_segments() {
    local prompt_id=$1
    local num_segments=${#SEGMENTS[@]}

    # Iterate over the segments in the array by index.
    for (( segcnt = 1; segcnt <= $num_segments; segcnt++ )) do
        # debug "segment $prompt_id $segcnt"

        # Split the current segment into a ';' delimited array.
        segparts=(${(s:;:)SEGMENTS[$segcnt]})
        #segparts=(`echo $SEGMENTS[$segcnt] | tr ";" "\n"`)

        # Assemble the segment string.
        segment="%K{$segparts[2]}%F{$segparts[3]} $segparts[1] "

        # The separator is always written after the content for the left prompt.
        if [[ $prompt_id -eq 0 ]]; then

            # If we're drawing the last segment on the left, set the background
            # to the default, otherwise, use the content's background from the
            # next segment.
            if [[ $segcnt -eq $num_segments ]]; then
                segment="$segment%K{0}"
            else
                (( nsegcnt = $segcnt + 1 ))
                nsegparts=(${(s:;:)SEGMENTS[$nsegcnt]})
                #nsegparts=(`echo $SEGMENTS[$nsegcnt] | tr ";" "\n"`)
                segment="$segment%K{$nsegparts[2]}"
            fi

            # The separators foreground color needs to match the background color
            # for the current segment's content.
            segment="$segment%F{$segparts[2]}"

            # Add the separator to the end of the segment.
            segment="$segment$LSEP"

        # The separator is always written before the content for the right prompt.
        elif [[ $prompt_id == 1 ]]; then

            # Add the separator to the front of the segment.
            segment="$RSEP$segment"

            # If we're drawing the first segment on the right-hand side, set the
            # segment separators background color to the default. Otherwise, use
            # the background color of the previous segment's content.
            if [[ $segcnt -eq 0 ]]; then
                segment="%K{0}$segment"
            else
                (( psegcnt = $segcnt - 1 ))
                psegparts=(${(s:;:)SEGMENTS[$psegcnt]})
                #psegparts=(`echo $SEGMENTS[$psegcnt] | tr ";" "\n"`)
                segment="%K{$psegparts[2]}$segment"
            fi

            # The separator's foreground color needs to match the background color
            # of the current segment's content.
            segment="%F{$segparts[2]}$segment"

        fi

        # And finally draw the assembled segment.
        echo -en "$segment"
    done
}


# Initialize Prompt
# -----------------
# Build & draw the prompt. Takes one argument, the prompt_id
# (0 = left prompt, 1 = right prompt).

function init_prompt() {
    # Initialize the prompt_id.
    local prompt_id=$1

    # Reset the segments array.
    SEGMENTS=()

    # Add segments for the left-hand prompt.
    if [[ $prompt_id -eq 0 ]]; then
        # debug "Adding left-prompt segments"
        # segment_test red
        # segment_test blue
        # segment_test yellow
        # segment_test green

        segment_error
        segment_context
        segment_path
        # segment_virtualenv

    # Add segments for the right-hand prompt.
    elif [[ $prompt_id -eq 1 ]]; then
        # debug "Adding right-prompt segments"
        # segment_test red
        # segment_test blue
        # segment_test yellow
        # segment_test green

        # segment_vc
        segment_timestamp
    fi

    # Draw the prompt segments.
    draw_segments $prompt_id
}

# PROMPT=$(build_prompt 0)
# RPROMPT=$(build_prompt 1)
PROMPT='%{%f%b%k%}$(init_prompt 0)%{%f%b%k%}'
RPROMPT='%{%f%b%k%}$(init_prompt 1)%{%f%b%k%}'
