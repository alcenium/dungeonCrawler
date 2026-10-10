#! /bin/sh
tmux new-session -d -s pygame -n editor
tmux new-window -t pygame:2 -n terminal
tmux send-key -t pygame:2 'source ./activate.sh && clear' C-m
tmux last-window -t pygame
tmux send-key -t pygame 'nvim main.py' C-m
tmux send-key -t pygame ' h'
tmux attach-session -t pygame
