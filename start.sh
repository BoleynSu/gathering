#!/bin/bash
root=`dirname \`realpath $0\``

nohup $root/gathering.py >> $root/gathering.log &
echo $! > $root/gathering.pid

