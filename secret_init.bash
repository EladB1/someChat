#!/bin/bash

function prompt_about_file() {
  file_=$1
  acceptable_ans=1
  while [[ $acceptable_ans -eq 1 ]]; do
    read -p "File $file_ exists. Do you want to overwrite it? [y/N] " answer
    if [[ $answer = 'y' || $answer = 'N' ]]; then
      acceptable_ans=0
    fi
  done
  echo $answer
}

function write_pw_to_file() {
  file_=$1
  pw_len=$2
  echo "Writing to file $file_" 
  echo $(pwgen -1snc $pw_len) > $file_
}

function handle_file() {
  file_=$1
  pw_len=$2
  if [[ -f $file_ ]]; then
    ans=$(prompt_about_file $file_)
    if [[ $ans = 'y' ]]; then
      write_pw_to_file $file_ $pw_len
    else
      echo 'Nothing left to do'
    fi
  else
    write_pw_to_file $file_ $pw_len
  fi
}

if [[ ! -d .env ]]; then
  mkdir .env
fi

# Super database user
handle_file .env/.pguser.txt 16

# App database user
handle_file .env/.appuser.txt 16



