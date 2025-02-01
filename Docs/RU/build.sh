#!/bin/sh

set -euf

# Include https://github.com/SixArm/posix-shell-script-kit
. "$(dirname "$(readlink -f "$0")")/scripts/posix-shell-script-kit"

# Preflight

command_exists_or_die "pandoc"
command_exists_or_die "xelatex"

# Choose fonts

mainfont="Arial"
sansfont="Arial"
monofont="Arial"
mathfont="Arial"

font_name_exists_or_die "$mainfont"
font_name_exists_or_die "$sansfont"
font_name_exists_or_die "$monofont"
font_name_exists_or_die "$mathfont"

# Main

DIR0=$(dirname "$0")

#pandoc \
#    --filter=scripts/filter.py \
#    -V linkcolor:blue \
#        -V geometry:b5paper \
#	    -V geometry:margin=2cm \
#	        -V mainfont="$mainfont" \
#		    -V sansfont="$sansfont" \
#		        -V monofont="$monofont" \
#			    -V mathfont="$mathfont" \
#			        -V fontsize=14pt \
#				    --pdf-engine=lualatex \
#										       "$@"


pandoc \
    --filter=scripts/filter.py \
    -V linkcolor:blue \
    -V geometry:b5paper \
    -V geometry:margin=2cm \
    -V mainfont="$mainfont" \
    -V sansfont="$sansfont" \
    -V monofont="$monofont" \
    -V mathfont="$mathfont" \
    -V fontsize=14pt \
    --pdf-engine=lualatex \
    --reference-doc=reference.docx \
    "$@"