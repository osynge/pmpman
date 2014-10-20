#!/bin/sh
# Design Requirements.
#
# This script must exit wihtout error if python cannot be launched
#




parrameters=$*
python_version="python"
pmpman_cli="pmpman_cli"

#python_version="pythonsss"

python_path=`which $python_version 2> /dev/null`
if [ "" = "${python_path}" ] ; then
# echo "DEBUG:$python_version not found in $path" 1>&2
# We should exit nicely if python is not found.
exit 0
fi
# echo "DEBUG:Found-${python_path}" 1>&2
pmpman_cli_path=`which $pmpman_cli 2> /dev/null`
if [ "" = "${pmpman_cli_path}" ] ; then
# we now fall back to local directory if not installed.
#echo "DEBUG:pmpman_cli_path not found:${pmpman_cli_path}" 1>&2
if [ ! -f "./${pmpman_cli}" ] ; then
#if [ test -f ./pmpman_cli ] ; then
echo "DEBUG:pmpman_cli_path not found:${pmpman_cli_path}" 1>&2
echo "ERROR:pmpman_cli_path not found:./${pmpman_cli}" 1>&2
exit 0
fi
pmpman_cli_path=`pwd`/${pmpman_cli}
fi
#echo "DEBUG:Found-pmpman_cli_path:${pmpman_cli_path}" 1>&2

wrapped_command="${python_path} ${pmpman_cli_path} ${parrameters}"
exec $wrapped_command

