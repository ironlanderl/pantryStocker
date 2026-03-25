#!/usr/bin/env bash

tmux new-window
tmux rename-window server
tmux send-keys 'fc -p' C-m # sets private history mode?
tmux send-keys 'cd backend' C-m
tmux send-keys 'source .venv/bin/activate' C-m
tmux send-keys 'fastapi dev --host 0.0.0.0' C-m

tmux split-window -v
tmux send-keys 'fc -p' C-m # sets private history mode?
tmux send-keys 'cd frontend' C-m
tmux send-keys './node_modules/vite/bin/vite.js' C-m
