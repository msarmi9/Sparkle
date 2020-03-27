# Get Sparkle's WatchOS and iOS apps running in your local `xcode`

1. `git clone https://github.com/msarmi9/Sparkle.git`

2. `cd Sparkle/`

3. `git checkout mobile`

4. `cd mobile/`

5. From here, we will be following the [aws-amplify](https://aws-amplify.github.io/docs/ios/storage#storage-access) docs to get your aws configurations set up locally From here, we will be following the [aws-amplify](https://aws-amplify.github.io/docs/ios/storage#storage-access) docs to get your aws configurations set up locally. If you do not already have the [node package manager](https://www.npmjs.com/get-npm), you should install it.

6. Next, install the `aws-amplify` cli from the commandline: `$ npm install -g @aws-amplify/cli`

7. Then, `amplify configure` to mark this as an amplify directory. It will prompt you to log in to the aws console, which you should do. After choosing the default region as `us-west-2`, you will be prompted to create a new aws user. Do so, making sure to enable programmatic access, and give all permissions from here: https://aws-amplify.github.io/docs/cli-toolchain/usage?sdk=js#iam-policy-for-the-cli

8. Then, give the promptings the accesskeys and it will create a new AWS profile for you to use.

9. Then run `$ amplify init`, with the following responses,

```
$ amplify init
Note: It is recommended to run this command from the root of your app directory
? Enter a name for the project mobile
? Enter a name for the environment mobileenv
? Choose your default editor: Vim (via Terminal, Mac OS only)
? Choose the type of app that you're building ios
Using default provider  awscloudformation

For more information on AWS Profiles, see:
https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html

? Do you want to use an AWS profile? Yes
? Please choose the profile you want to use Sparkle-amplify
Adding backend environment mobileenv to AWS Amplify Console app: d1aipq0q57wfdg
⠙ Initializing project in the cloud...

CREATE_IN_PROGRESS DeploymentBucket                AWS::S3::Bucket            Thu Mar 26 2020 16:57:03 GMT-0700 (Pacific Daylight Time) Resource creation Initiated
CREATE_IN_PROGRESS UnauthRole                      AWS::IAM::Role             Thu Mar 26 2020 16:57:03 GMT-0700 (Pacific Daylight Time) Resource creation Initiated
CREATE_IN_PROGRESS AuthRole                        AWS::IAM::Role             Thu Mar 26 2020 16:57:03 GMT-0700 (Pacific Daylight Time) Resource creation Initiated
CREATE_IN_PROGRESS UnauthRole                      AWS::IAM::Role             Thu Mar 26 2020 16:57:02 GMT-0700 (Pacific Daylight Time)
CREATE_IN_PROGRESS DeploymentBucket                AWS::S3::Bucket            Thu Mar 26 2020 16:57:02 GMT-0700 (Pacific Daylight Time)
CREATE_IN_PROGRESS AuthRole                        AWS::IAM::Role             Thu Mar 26 2020 16:57:02 GMT-0700 (Pacific Daylight Time)
CREATE_IN_PROGRESS amplify-mobile-mobileenv-165657 AWS::CloudFormation::Stack Thu Mar 26 2020 16:56:59 GMT-0700 (Pacific Daylight Time) User Initiated
⠸ Initializing project in the cloud...

CREATE_COMPLETE UnauthRole AWS::IAM::Role Thu Mar 26 2020 16:57:17 GMT-0700 (Pacific Daylight Time)
CREATE_COMPLETE AuthRole   AWS::IAM::Role Thu Mar 26 2020 16:57:17 GMT-0700 (Pacific Daylight Time)
⠧ Initializing project in the cloud...

CREATE_COMPLETE DeploymentBucket AWS::S3::Bucket Thu Mar 26 2020 16:57:24 GMT-0700 (Pacific Daylight Time)
⠴ Initializing project in the cloud...

CREATE_COMPLETE amplify-mobile-mobileenv-165657 AWS::CloudFormation::Stack Thu Mar 26 2020 16:57:27 GMT-0700 (Pacific Daylight Time)
✔ Successfully created initial AWS cloud resources for deployments.
✔ Initialized provider successfully.
Initialized your environment successfully.

Your project has been successfully initialized and connected to the cloud!

Some next steps:
"amplify status" will show you what you've added already and if it's locally configured or deployed
"amplify add <category>" will allow you to add features like user login or a backend API
"amplify push" will build all your local backend resources and provision it in the cloud
“amplify console” to open the Amplify Console and view your project status
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud

Pro tip:
Try "amplify add api" to create a backend API and then "amplify publish" to deploy everything

```

10. then `$ amplify add storage` with the following prompts

```
$ amplify add storage
? Please select from one of the below mentioned services: Content (Images, audio, video, etc.)
? You need to add auth (Amazon Cognito) to your project in order to add storage for user files. Do you want to add auth now? Yes
Using service: Cognito, provided by: awscloudformation

 The current configured provider is Amazon Cognito.

 Do you want to use the default authentication and security configuration? Default configuration
 Warning: you will not be able to edit these selections.
 How do you want users to be able to sign in? Username
 Do you want to configure advanced settings? No, I am done.
Successfully added auth resource
? Please provide a friendly name for your resource that will be used to label this category in the project: amplifyFriendly
? Please provide bucket name: amplifyfriendlybucket
? Who should have access: Auth and guest users
? What kind of access do you want for Authenticated users? create/update, read
? What kind of access do you want for Guest users? create/update, read
? Do you want to add a Lambda Trigger for your S3 Bucket? No
Successfully updated auth resource locally.
Successfully added resource amplifyFriendly locally

Some next steps:
"amplify push" builds all of your local backend resources and provisions them in the cloud
"amplify publish" builds all of your local backend and front-end resources (if you added hosting category) and provisions them in the cloud
```

11. And finally `$ amplify push` which will create `amplifyconfiguration.json` and `awsconfiguration.json`

12. Now install [`cocoapods`](https://guides.cocoapods.org/using/getting-started.html), which is a dependency manager for xcode projects. On the off-chance that you've been using cocoapods recently, you **need to** clear your pods cache (this has been such a headache)! `$ rm -rf "${HOME}/Library/Caches/CocoaPods" && rm -rf "`pwd`/Pods/"`.

13. Now install all the projects' dependencies (as listed in the `Podfile`) with `$ pod install --repo-update`. This may take a moment. It generates the `Podfile.lock` and the `Pods/` directory.

14. Now, open up the project, specifically using the `.xcworkspace` file. In other words, type the following on the commandline: `$ open mobile.xcworkspace` (this assumes you have xcode installed)

15. For this portion, we have to drag our aws config files into xcode manually.

* Open the finder of your project and drag the `amplifyconfiguration.json` and `awsconfiguration.json` over to the Xcode window, under the workspace.
* Enable Copy items if needed if not already enabled
* For “Added folders”, have Create groups selected.
* For “Add to targets”, make sure the app target is checked off.

16. Now, you should be good to go to build and run the apps in xcode! 
