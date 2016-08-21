#!/bin/bash
# Created using gbash.py

err() {
    local FAIL="\033[91m"
    local END="\033[0m"
    local msg="$1"
    echo -e "$FAIL$msg$END" >&2
}

show_help() {
cat << EOF
Joins multiple pdf with bookmarks named after file names.
Usage: ${0##*/} [-a|-i <'@' joined file names>]  -r <'@' joined file names> -o <fileName>

    -a	short hand for `ls -X1 | tr -t '\n' '@'`
    -i	takes '@' joined file list like "a.pdf@b.pdf@c.pdf"
    -r	replaces file name from -i list with this list (position wise)
    -o	Joins all pdf into this file
EOF
}

dump_input() {
    local PARSER=$(python -c "import sys; print( 'urllib.parse' if (sys.version_info[0] == 3) else 'urllib' )")
    python -c "import $PARSER; print($PARSER.unquote('3%0A1%0Aa%0Aautolist%0Ashort%20hand%20for%20%60ls%20-X1%20%7C%20tr%20-t%20%27%5Cn%27%20%27%40%27%60%0A%0A2%0Ai%0Ainput_files%0A%3C%27%40%27%20joined%20file%20names%3E%0Atakes%20%27%40%27%20joined%20file%20list%20like%20%22a.pdf%40b.pdf%40c.pdf%22%0A%0A0%0A%0A2%0Ar%0Areplace_names%0A%3C%27%40%27%20joined%20file%20names%3E%0Areplaces%20file%20name%20from%20-i%20list%20with%20this%20list%20%28position%20wise%29%0A%0A2%0Ao%0Aoutput_file%0A%3CfileName%3E%0AJoins%20all%20pdf%20into%20this%20file%0A%0A0%0Apdfjoin.sh%0AJoins%20multiple%20pdf%20with%20bookmarks%20named%20after%20file%20names.'))"
}


autolist() {
    err "Unimplemented -a (autolist)"
}

input_files() {
    local param_input_files=$1
    err "Unimplemented -i (input_files) with param $param_input_files"
}

replace_names() {
    local param_replace_names=$1
    err "Unimplemented -r (replace_names) with param $param_replace_names"
}

output_file() {
    local param_output_file=$1
    err "Unimplemented -o (output_file) with param $param_output_file"
}



optStage_0=true

if [ "$1" == "--dumpinput" ]; then
    dump_input >&1
    exit 0
fi

GETOPT_RAN=false
while getopts ":ai:r:o:" opt; do
    GETOPT_RAN=true
    case $opt in 
        a)
            if [ "$optStage_0" = true ] ; then
                optStage_0=false
                autolist
            else
                err "Only one in a, i is allowed, ignoring -$opt $OPTARG"
            fi
            ;;
        i)
            if [ "$optStage_0" = true ] ; then
                optStage_0=false
                input_files "$OPTARG"
            else
                err "Only one in a, i is allowed, ignoring -$opt $OPTARG"
            fi
            ;;
        r)
            replace_names "$OPTARG"
            ;;
        o)
            output_file "$OPTARG"
            ;;
        \?)
            err "Invalid option: -$OPTARG"
            show_help >&2
            exit 1
            ;;
        :)
            err "Option -$OPTARG requires an argument."
            show_help >&2
            exit 1
            ;;
    esac
done

if [ "$GETOPT_RAN" = false ] ; then
    show_help >&2
    exit 1
fi

## Copy to create shorthand for /dev/stdout or /dev/stdin using hyphen "-"
#     if [ "$1" == "-" ]; then
#         OUTPUT_FILE="/dev/stdout"
#     else
#         if [ -z "$1" ]; then
#             OUTPUT_FILE="/dev/stdout"
#         else
#             OUTPUT_FILE=$1
#         fi
#     fi

