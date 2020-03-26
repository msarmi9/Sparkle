#! /bin/sh

echo "3\nSparkle_web_automated\nY\n1\nN\nn\n" | cat /dev/stdin | eb init -i


eb create Sparkle-web-automated-env


aws codepipeline create-pipeline --cli-input-json file://pipeline.json --profile AWS_test2
