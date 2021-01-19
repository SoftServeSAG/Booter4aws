
#!/bin/bash

# This script will create the AWS infrastructure required to launch the demo, as well as future multi-robot apps.
BASE_DIR=`pwd`
ROS_APP_DIR=$BASE_DIR/simulation_ws
LAUNCHER_APP_DIR=$BASE_DIR/setup
STACK_NAME=cr2-robomaker-fleet-cicd
CURRENT_STACK=.current-aws-stack-cicd

STACK_NAME_BUCKET=cr2-robomaker-fleet-cicd-bucket
CURRENT_STACK_BUCKET=.current-aws-stack-cicd-bucket

S3_OUTPUT_KEY=cr2multirobot/bundle/output.tar


#S3_BUCKET=yfedi-test-bucket

export AWS_DEFAULT_REGION=us-east-2

sudo pip3 install boto3==1.14.28 > /dev/null

# Setup AWS resources for the application
if [ ! -f "$CURRENT_STACK" ]; then
  # Deploy base stack (NOTE: This will NOT deploy the SAM-based Lambda function. To do that, follow the instructions in the README.)
  aws cloudformation deploy --template-file $LAUNCHER_APP_DIR/robomaker_cicd_bucket.yml --stack-name $STACK_NAME_BUCKET --capabilities CAPABILITY_NAMED_IAM
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME_BUCKET && echo "stackname=$STACK_NAME_BUCKET" > .current-aws-stack
fi

# Upload the application bundle. 
s3Bucket=$(aws cloudformation describe-stacks --stack-name $STACK_NAME_BUCKET --query "Stacks[0].Outputs[?OutputKey=='RoboMakerCICDS3Bucket'].OutputValue" --output text)
if $s3Bucket==None 
then
 echo "Please ensure that bucket for CICD exists."
 exit
fi

echo "Uploading lambda functions to the bucket"

cd $LAUNCHER_APP_DIR/checkStatus/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$s3Bucket/lambdas/checkStatus/

cd $LAUNCHER_APP_DIR/errorLaunchingSimulations/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$s3Bucket/lambdas/errorLaunchingSimulations/

cd $LAUNCHER_APP_DIR/processAndLaunchBatchSimulations/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$s3Bucket/lambdas/processAndLaunchBatchSimulations/

cd $LAUNCHER_APP_DIR/sendSimSummary/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$s3Bucket/lambdas/sendSimSummary/

cd $LAUNCHER_APP_DIR/triggerStepFunctions/
zip $LAUNCHER_APP_DIR/function.zip ./*
aws s3 mv $LAUNCHER_APP_DIR/function.zip s3://$s3Bucket/lambdas/triggerStepFunctions/

# Setup AWS resources for the application
if [ ! -f "$CURRENT_STACK" ]; then
  # Deploy base stack (NOTE: This will NOT deploy the SAM-based Lambda function. To do that, follow the instructions in the README.)
  aws cloudformation deploy --template-file $LAUNCHER_APP_DIR/robomaker_cloudformation_with_lambdas.yml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM --parameter-overrides SimulationApplicationS3Key=$S3_OUTPUT_KEY CICDS3Bucket=$s3Bucket
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME && echo "stackname=$STACK_NAME" > .current-aws-stack
fi
