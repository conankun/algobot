# Prerequisite: Set discord token as MANDOO_BOT_TOKEN environment variable.
export current_version=$(date +%s)
export zip_file_name="algobot_${current_version}.zip"
zip -r "${zip_file_name}" . -x '.DS_STORE' '.idea/*' '.terraform/' '.terraform*' '*.sh' '*.tf' '.git/*' '*/__pycache__/*'
aws s3 cp "${zip_file_name}" "s3://algobot67/${zip_file_name}"
rm "${zip_file_name}"
terraform apply -var "zip_file_name=${zip_file_name}" -var "discord_bot_token=${ALGO_BOT_TOKEN}" -var "aws_access_key_id=${AWS_ACCESS_KEY_ID}" -var "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}"
