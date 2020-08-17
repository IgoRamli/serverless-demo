#! /bin/bash

files=($(find . -type f -regex "^.*yaml$"))

for i in "${files[@]}"
do
    eval "kubectl apply -f ${i}"
done