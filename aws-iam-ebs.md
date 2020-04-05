# How to get things working

Interestingly, to my knowledge at the moment, it is not possible to create and launch this app _the first time_ entirely from the command line. There are 3 main commands that need to be executed, but they have interdependent pieces that require individual verification.

1. Matt attaches the `AWSElasticBeanstalkFullAccess` and `AWSCodePipelineFullAccess` policies to our iam accounts

2. Collin runs `echo -e "3\nSparkle\nY\n1\nN\nn\n" | eb init -i --profile collinprather@msds-iam` (under the msds603 conda env), which does the following:
    - creates EBS application called "Sparkle" (without an environment)
    - creates an s3 bucket to dump EBS files which should have a name like `elasticbeanstalk-us-west-2-678524477173`. _Note: to delete this bucket (even from a root account) you must edit the bucket policy to allow that action_.

3. Collin runs `eb create Sparkle-env --profile collinprather@msds-iam`, which creates a ton of stuff but here are the most notable:
    - create EBS env called `Sparkle-env` 
    - creates (I believe) 4 new service roles: `aws-elasticbeanstalk-ec2-role`, `aws-elasticbeanstalk-service-role`, `AWSServiceRoleForAutoScaling`, `AWSServiceRoleForElasticLoadBalancing`
    - Launches an ec2 instance called `Sparkle-env` (I believe the "elastic load balancing" will automatically spin up new instances if necessary
    - web app should now be running!

4. Matt goes to https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create-service-role-console.html (logged into root account)  and follows instructions in console to manually create a pipeline. (could not figure out how to make a service role under iam account, but there probably is a way). This should do the following
    - Create a policy called: `AWSCodePipelineServiceRole-us-west-2-Sparkle-Pipeline`
    - creates an s3 bucket with a name similar to `codepipeline-us-west-2-375147072177`
    - Creates a service role with a name similar to `AWSCodePipelineServiceRole-us-west-2-Sparkle-Pipeline`
    - Now any new pushes to the master branch will automatically update our live app!
