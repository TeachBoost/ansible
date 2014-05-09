#!/bin/bash
#
# installation script
# creates local configuration files and sets up the environment

# get the paths
rootpath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
apppath="$rootpath/..";

# copy the config environment file
env=${1:-"local"}

if [ ! -f "${apppath}/deploy/env/${env}" ] ; then
    printf "Invalid environment specified: %s\n" "$env" >&2
    exit 1
fi

echo "Copying default '${env}' config file"
cp ${apppath}/deploy/env/${env} ${apppath}/deploy/config.py

# read in the secret file (if there is one). we want to
# iterate line by line looking for VAR=val lines. Then,
# we'll find ##VAR## in the local config file and replace
# it with val.
if [[ -f "${apppath}/deploy/secret.ini" ]] ; then
    while read -r line || [[ -n $line ]]
    do
        IFS='=' read -ra ARR <<< "$line"
        find=${ARR[0]}
        replace=${ARR[1]}
        sed -i "s/##${find}##/${replace}/g" ${apppath}/deploy/config.py
    done < "${apppath}/deploy/secret.ini"
else
    touch "${apppath}/deploy/secret.ini"
fi

echo ''
echo 'Done! Make sure you run the SQL statements.'
echo 'For help, run ./update_sql_db.sh -h'

