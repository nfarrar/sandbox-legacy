#!/usr/bin/env bash

echo -e "\e[31m             \rred/default     (user defined, slash-e escape)"
echo -e "\033[32m           \rgreen/default   (user defined, octal escape)"
echo -e "\x1b[31;42m        \rred/green       (user defined, hex escape)"
echo -e "\x1b[30m           \rblack/green     (bleeding from previous line)"
echo -e "\x1b[0;34m         \rblue/default    (inline clear)"
echo -e "\x1b[38;5;9m       \rred/default     (user defined red using xterm index)"
echo -e "\e[38;5;196m       \rred/default     ('full' red from xterm index)"
echo -e "\e[38;2;255;0;0;m  \rred/default     ('full' red using rgb)"
printf "\x1b[0;31m          \rred/default     (with printf)\n"

