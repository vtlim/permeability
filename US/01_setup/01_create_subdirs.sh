#!/bin/sh

# Purpose: create subdirs for umbrella sampling.
# Usage: in terminal, "file.sh directory number"
# Example: "file.sh output 20"
# Note: This script creates n+1 dirs (incl 00/).



cd /pub/limvt/pmf/07_us
#cd /home/victoria/Documents/pmf/07_us

# make sure directory does not exist
if [ -d "$1" ]; then
  echo "The directory '$1' already exists! Exiting."
  exit 1
fi

mkdir $1



n=0;
while [ "$n" -le "$2" ]; do

  if [ $n -lt 10 ]; then
      mkdir "$1/0$n"
      mkdir "$1/0$n/01_min"
  else 
      mkdir "$1/$n"
      mkdir "$1/$n/01_min"
  fi

  n=`expr "$n" + 1`;
done
