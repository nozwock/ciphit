#!/usr/bin/zsh
DIR="~/.cpt"
SDIR="~/.cpt/cpt"
CMD="alias cpt='python ~/.cpt/cpt/__init__.py'"

function start() {
	echo -e "\\n  ▓▓▓▓▓▓▓▓▓▓▓▓"
	echo -e " ░▓    about ▓ cpt"
	echo -e " ░▓   author ▓ sgrkmr"
	echo -e " ░▓     code ▓ local"
	echo -e " ░▓▓▓▓▓▓▓▓▓▓▓▓"
	echo -e " ░░░░░░░░░░░░\\n"
}

function ask() {
	# https://djm.me/ask
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

		echo -e -n "$1 [$prompt] "
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

function install() {
	function prep() {
		echo -e "\\e[32m[ cpt ]\\e[m copying files"
		eval "mkdir -p $SDIR"
		eval "cp -t $SDIR __main__.py __init__.py"
		echo -e "\\e[32m[ cpt ]\\e[m creating aliases"
		touch ~/.bashrc ~/.zshrc
		grep -qxF "$CMD" ~/.bashrc || echo $CMD  >> ~/.bashrc
		grep -qxF "$CMD" ~/.zshrc || echo $CMD >> ~/.zshrc
		source ~/.bashrc && source ~/.zshrc
		if ask "\\e[32m[ finished ]\\e[m would you like to install pycrypto & asciimatics (requires pip)?" Y; then
			command python3 -m pip install pycrypto asciimatics
		fi
		echo -e "\\e[32m[ warning ]\\e[m please restart termux to apply changes"
	}
	cd "$(dirname "${BASH_SOURCE[0]}")"
	if eval "[ -d $DIR ]"; then
		echo -e "\\e[32m[ cpt ]\\e[m found, reinstalling cpt"
        	eval "rm -rf $DIR"
		prep
	else
		echo -e "\\e[32m[ cpt ]\\e[m not found, installing cpt"
		prep
	fi
}

function remove() {
	if eval "[ -d $DIR ]"; then
		echo -e "\\e[32m[ cpt ]\\e[mfound, removing cpt"
		eval "rm -rf $DIR"
		echo -e "\\e[32m[ cpt ]\\e[m removing aliases"
		sed -i '/alias cpt/d' ~/.bashrc
		sed -i '/alias cpt/d' ~/.zshrc
		echo -e "\\e[32m[ warning ]\\e[m please restart termux to apply changes"
	else
		echo -e "\\e[32m[ cpt ]\\e[m not found, aborting"
		exit
	fi
}

while [[ $# -gt 0 ]]; do
	case $1 in
	-r | --remove)
		rem=true
		;;
	*) echo -e "Unknown options:' $1" ;;
	esac
	shift
done

start
if [ $rem ]; then
	remove
else
	install
fi
exit
