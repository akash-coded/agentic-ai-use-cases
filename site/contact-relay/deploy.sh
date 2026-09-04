#!/usr/bin/env bash
# Deploy (or update) the contact relay into the AWS account your CLI is signed in to.
#
#   NOTIFY_EMAIL=you@example.com ALLOWED_ORIGIN=https://you.github.io ./deploy.sh
#
# Needs: AWS CLI v2 with credentials that can create CloudFormation, Lambda, IAM, DynamoDB, SES and S3.
# Region comes from AWS_REGION / AWS_DEFAULT_REGION / your profile (falls back to us-east-1).
set -euo pipefail
cd "$(dirname "$0")"

STACK="${STACK:-skyways-contact-relay}"
NOTIFY_EMAIL="${NOTIFY_EMAIL:-mfs.akash@gmail.com}"
ALLOWED_ORIGIN="${ALLOWED_ORIGIN:-https://akash-coded.github.io}"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-$(aws configure get region 2>/dev/null || true)}}"
REGION="${REGION:-us-east-1}"
ACCOUNT="$(aws sts get-caller-identity --query Account --output text)"
BUCKET="cfn-artifacts-${ACCOUNT}-${REGION}"

echo "account ${ACCOUNT} · region ${REGION} · stack ${STACK}"
echo "notify  ${NOTIFY_EMAIL} · origin ${ALLOWED_ORIGIN}"

if ! aws s3api head-bucket --bucket "$BUCKET" --region "$REGION" 2>/dev/null; then
  echo "creating artifact bucket s3://${BUCKET}"
  aws s3 mb "s3://${BUCKET}" --region "$REGION" >/dev/null
  aws s3api put-public-access-block --bucket "$BUCKET" --region "$REGION" \
    --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
fi

aws cloudformation package \
  --template-file template.yaml --s3-bucket "$BUCKET" --s3-prefix "$STACK" \
  --output-template-file .packaged.yaml --region "$REGION" >/dev/null

aws cloudformation deploy \
  --template-file .packaged.yaml --stack-name "$STACK" --region "$REGION" \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --no-fail-on-empty-changeset \
  --parameter-overrides "NotifyEmail=${NOTIFY_EMAIL}" "AllowedOrigin=${ALLOWED_ORIGIN}" \
    "CreateEmailIdentity=${CREATE_EMAIL_IDENTITY:-true}"

echo
aws cloudformation describe-stacks --stack-name "$STACK" --region "$REGION" \
  --query "Stacks[0].Outputs[].[OutputKey,OutputValue]" --output table
echo
echo "Next: click the SES verification link in ${NOTIFY_EMAIL}, then put FunctionUrl into site/frame/config.js."
