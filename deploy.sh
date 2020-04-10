#! /bin/sh

#### Initializing EBS ####
# assumptions: user has awsebcli,
#              necessary aws credentials,
#              there is no .elasticbeanstalk folder in directory, 
#              aws account has no other beanstalk applications
echo -e "3\nSparkle\nY\n1\nN\nn\n" | eb init -i --profile Sparkle-EBS-CodePipeline


#### Creating ebs env ####
# uploads all files up to EBS (except those in .ebignore)
# note: currently not making a worker env
eb create Sparkle-env --profile Sparkle-EBS-CodePipeline


#### Creating CodePipeline ####
# 1) follow instructions here: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create-service-role-console.html
#       - meaning, create the pipeline, which creates the service role
# 2) Attach the CodePipelineFullAccess policy to our iam
# 3) update the pipeline.json so that it has correct arn, s3 location, github OAuth tokens, and application/env name
# assumptions: arn has correct permissions (CodePipeline and S3)
#              aws account/profile has correct permissions
#              

aws codepipeline create-pipeline --cli-input-json file://pipeline.json --profile Sparkle-EBS-CodePipeline
