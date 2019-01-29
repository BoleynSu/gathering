#!/bin/bash
root=`dirname \`realpath $0\``

kill `cat $root/gathering.pid`
rm $root/gathering.pid

