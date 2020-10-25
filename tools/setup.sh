#!/bin/sh
set -e

# Default settings
CIPHIT=~/.ciphit
PKG_DIR=$CIPHIT/ciphit
TMP=$(dirname $0)
if [ ${TMP##*/} != . ]; then
	SOURCE_DIR=$(dirname "$(dirname $0)")/ciphit
else
	SOURCE_DIR=../ciphit
fi
ALIAS_CMD="alias ciphit="
ALIAS_CPT=$ALIAS_CMD\'"python "$CIPHIT\'

error() {
	echo ${RED}"Error: $@"${RESET} >&2
}

cli_help() {
	cli_name=${0##*/}
	echo "Usage: $cli_name [INSTALL, DEFAULT] [OPTIONS]

Options:
\t-h, --help
\t-r, --remove"
	exit 1
}

setup_color() {
	# Only use colors if connected to a terminal
	if [ -t 1 ]; then
		RED=$(printf '\033[31m')
		GREEN=$(printf '\033[32m')
		YELLOW=$(printf '\033[33m')
		BLUE=$(printf '\033[34m')
		BOLD=$(printf '\033[1m')
		RESET=$(printf '\033[m')
	else
		RED=""
		GREEN=""
		YELLOW=""
		BLUE=""
		BOLD=""
		RESET=""
	fi
}

ask() {
	local prompt default reply

	while true; do

		if [ "${2:-}" = "Y" ]; then
			prompt="Y/n"
			default=Y
		elif [ "${2:-}" = "N" ]; then
			prompt="y/N"
			default=N
		else
			prompt="y/n"
			default=
		fi

		echo -n "$1 [$prompt] "
		read -r reply </dev/tty

		if [ -z "$reply" ]; then
			reply=$default
		fi

		case "$reply" in
		Y* | y*) return 0 ;;
		N* | n*) return 1 ;;
		esac

	done
}

setup_ciphit() {
	if [ -d $CIPHIT ]; then
		echo "${YELLOW} You already have ciphit installed.${RESET}"
	else
		echo "${cpt_tag} Installing ciphit"
		echo "${cpt_tag} Copying files"
		mkdir -p $PKG_DIR
		cp -rt $PKG_DIR $SOURCE_DIR/*
		
		# Generating __main__.py
		cat > $CIPHIT/__main__.py << EOF
#!/usr/bin/env python
from ciphit.ciphit import main

if __name__ == "__main__":
	main()
EOF
		
		echo "${cpt_tag} Creating aliases"
		touch ~/.bashrc ~/.zshrc
		grep -sF $ALIAS_CMD ~/.bashrc  || echo $ALIAS_CPT  >> ~/.bashrc
		grep -sF $ALIAS_CMD ~/.zshrc || echo $ALIAS_CPT >> ~/.zshrc

		if ask "${cpt_tag} Do you want to install dependencies now?" N; then
			command python3 -m pip install -r requirements.txt
		fi
		echo "${GREEN}[ installed ]${RESET} Please restart shell to apply changes"
	fi
}

remove() {
	if [ -d $CIPHIT ]; then
		echo "${cpt_tag} Removing ciphit"
		rm -rf $CIPHIT
		echo "${cpt_tag} Removing aliases"
		sed -i "/$ALIAS_CMD/d" ~/.bashrc
		sed -i "/$ALIAS_CMD/d" ~/.zshrc
		echo "${RED}[ removed ]${RESET} Please restart shell to apply changes"
	else
		echo "${YELLOW}ciphit couldn't be found.${RESET}"
		exit 1
	fi
}

main() {
	local cpt_tag
	setup_color

	cpt_tag="${YELLOW}[ ciphit ]${RESET}"

	if [ $# -gt 1 ]; then
		error "expecting 1 parameter. Please see option --help"
		exit 1
	fi

	# Parsing args
	while [ $# -gt 0 ]; do
		case $1 in
		-r | --remove)
			remove=true
			;;
		-h | --help)
			help=true
			;;
		*) error "no such option: $1"
			exit 1
			;;
		esac
		shift
	done

	if [ $help ]; then
		cli_help
	elif [ $remove ]; then
		remove
	elif [ $# = 0 ]; then
		setup_ciphit
	fi
}

main "$@"