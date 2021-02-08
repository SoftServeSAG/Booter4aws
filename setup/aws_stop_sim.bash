
#!/bin/bash

# This script will create the AWS infrastructure required to launch the demo, as well as future multi-robot apps.
BASE_DIR=`pwd`
LAUNCHER_APP_DIR=$BASE_DIR/setup

echo "Cancel simulation jobs"
python3 $LAUNCHER_APP_DIR/stop_sim.py
echo "Done"