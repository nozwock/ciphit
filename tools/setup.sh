#!/bin/sh
set -e
export WORKDIR=$(cd $(dirname $0) && pwd)
. "$WORKDIR/commands/install"
. "$WORKDIR/commands/uninstall"

# Default settings
CIPHIT=~/.ciphit
PKG_DIR=$CIPHIT/ciphit
SOURCE_DIR=$(dirname $WORKDIR)/ciphit
ALIAS_CMD="alias ciphit="
ALIAS_CPT=$ALIAS_CMD\'"python "$CIPHIT\'

error() {
	echo ${RED}"Error: $@"${RESET} >&2
}

setup_color() {
	# Only use colors if connected to a terminal
	if [ -t 1 ]; then
		RED='\033[1;31m'
		GREEN='\033[1;32m'
		YELLOW='\033[1;33m'
		BLUE='\033[1;34m'
		BOLD=''
		RESET='\033[m'
	else
		RED=""
		GREEN=""
		YELLOW=""
		BLUE=""
		BOLD=""
		RESET=""
	fi
}

cli_help() {
	cli_name=${0##*/}
	echo "Usage: $cli_name [INSTALL, DEFAULT] [COMMANDS] [OPTIONS]

Commands:
\tu, uninstall

Options:
\t-h, --help"
	exit 1
}

main() {
	local cpt_tag;
	setup_color

	cpt_tag="${YELLOW}[ ciphit ]${RESET}"

	if [ $# -gt 1 ]; then
		error "expecting 1 parameter. Please see option --help"
		exit 1
	fi

	# Parsing args
	if [ $# = 0 ]; then
		install
	else
	    case $1 in
		-h | --help)
		    cli_help
		    ;;
		u | uninstall)
		    uninstall
		    ;;
	    	*) error "no such option: $1"
		    exit 1
		    ;;
	    esac
	fi
}

main "$@"
