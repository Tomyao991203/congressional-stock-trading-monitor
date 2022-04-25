#! /bin/sh

mkdir .elasticbeanstalk
touch .elasticbeanstalk/config.yml
config="branch-defaults:
  bmspates_continuous_deploy:
    environment: $AWS_ENVIORNMENT
  develop:
    environment: $AWS_ENVIORNMENT
environment-defaults:
  $AWS_ENVIORNMENT:
    branch: null
    repository: null
global:
  application_name: Congressional Stock Trading Monitor
  branch: null
  default_ec2_keyname: aws-eb
  default_platform: Docker
  default_region: us-east-1
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  profile: eb-cli
  repository: null
  sc: git
  workspace_type: Application"

printf "$config" > .elasticbeanstalk/config.yml

mkdir ~/.aws/
touch ~/.aws/config
config="[profile eb-cli]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY

[default]
region = $AWS_DEFAULT_REGION"

printf "$config" > ~/.aws/config
