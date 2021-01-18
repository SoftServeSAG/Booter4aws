
#!/bin/bash

# This script will create the AWS infrastructure required to launch the demo, as well as future multi-robot apps.
BASE_DIR=`pwd`
ROS_APP_DIR=$BASE_DIR/simulation_ws
LAUNCHER_APP_DIR=$BASE_DIR/setup
STACK_NAME=yfedi-robomaker-fleet
CURRENT_STACK=.current-aws-stack_with_lambdas
S3_OUTPUT_KEY=cr2multirobot/bundle/output.tar
S3_BUCKET=yfedi-test-bucket

export AWS_DEFAULT_REGION=us-east-2

sudo pip3 install boto3==1.14.28 > /dev/null


cd $LAUNCHER_APP_DIR/checkStatus/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$S3_BUCKET/lambdas/checkStatus/

cd $LAUNCHER_APP_DIR/errorLaunchingSimulations/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$S3_BUCKET/lambdas/errorLaunchingSimulations/

cd $LAUNCHER_APP_DIR/processAndLaunchBatchSimulations/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$S3_BUCKET/lambdas/processAndLaunchBatchSimulations/

cd $LAUNCHER_APP_DIR/sendSimSummary/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$S3_BUCKET/lambdas/sendSimSummary/

cd $LAUNCHER_APP_DIR/triggerStepFunctions/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$S3_BUCKET/lambdas/triggerStepFunctions/

# Setup AWS resources for the application
if [ ! -f "$CURRENT_STACK" ]; then
  # Deploy base stack (NOTE: This will NOT deploy the SAM-based Lambda function. To do that, follow the instructions in the README.)
  aws cloudformation deploy --template-file $LAUNCHER_APP_DIR/robomaker_cloudformation_with_lambdas.yml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM --parameter-overrides SimulationApplicationS3Key=$S3_OUTPUT_KEY
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME && echo "stackname=$STACK_NAME" > .current-aws-stack
fi

# # Upload the application bundle. 
# s3Bucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='RoboMakerS3Bucket'].OutputValue" --output text)

# if [ ! $s3Bucket==None ] || [ -f "$ROS_APP_DIR/bundle/output.tar" ]
# then
#   echo "Uploading files..."
#   aws s3 cp $ROS_APP_DIR/bundle/output.tar s3://$s3Bucket/$S3_OUTPUT_KEY
# else
#   echo "Bundle could not be uploaded. Please ensure \"$ROS_APP_DIR/bundle/output.tar\" and the S3 bucket \"$s3Bucket\" exist."
#   exit
# fi

# read -t 5 -p "Press any key to launch the sample simulation, or Ctrl+c within 5 seconds to exit." some_key
# python3 $LAUNCHER_APP_DIR/fleetLauncherLambda/app.py $STACK_NAME 