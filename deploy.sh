#! /bin/sh

#### Initializing EBS ####
# assumptions: user has awsebcli,
#              necessary aws credentials,
#              there is no .elasticbeanstalk folder in directory, 
#              aws account has no other beanstalk applications
# echo -e "3\nSparkle_web_automated\nY\n1\nN\nn\n"  | eb init -i
echo "3\nSparkle_web_automated\nY\n1\nN\nn\n" | cat /dev/stdin  | eb init -i


#### Creating ebs env ####
# note: currently not making a worker env
eb create Sparkle-web-automated-env


#### Creating CodePipeline ####
# assumptions: arn has correct permissions (CodePipeline and S3)
#              aws account/profile has correct permissions
#              
aws codepipeline create-pipeline --cli-input-json file://pipeline.json
