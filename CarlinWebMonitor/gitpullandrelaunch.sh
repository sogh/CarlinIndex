#Grab new code
git pull
#compile new code
/bin/play-2.1.1/play clean compile stage
#kill web server if running
if [ -f RUNNING_PID ];
then
    echo "Server running. Killing it first."
    kill -9 `cat RUNNING_PID`
    rm -rf RUNNING_PID
fi
#Launch updated web server
target/start &

