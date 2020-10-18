#/bin/bash

# starts the server, then, if there are new commits on the remote, kills the server, pull, restarts the server

set -eux

trap "exit" INT TERM ERR
trap "kill 0" EXIT

./main.py &
SERVER_PID=$!

while true; do
    git fetch
    NUM_COMMITS_AVAILABLE=$(git rev-list HEAD...origin/master --count)

    if [[ $NUM_COMMITS_AVAILABLE > 0 ]]; then

        git stash
        git pull --rebase
        git stash pop
        
        kill $SERVER_PID || true
        ./main.py &
        SERVER_PID=$!
    fi

    sleep 5
done
