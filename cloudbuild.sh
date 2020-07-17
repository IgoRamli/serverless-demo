# Run this in ./serverless-store folder in case cloudbuild.yaml is broken.

echo "Y" | gcloud app deploy app/app.yaml
echo "Y" | gcloud app deploy extras/streamEventsApp/app.yaml
echo "y" | gcloud functions deploy automl --source=./functions/automl/ --runtime=python37 --trigger-topic=new-product --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy detect_labels --source=./functions/detect_labels/ --runtime=python37 --trigger-topic=new-product --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy pay_with_stripe --source=./functions/pay_with_stripe/ --runtime=python37 --trigger-topic=payment-process --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy sendOrderConfirmation --source=./functions/sendOrderConfirmation/ --runtime=nodejs10 --trigger-topic=payment-completion --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy sendReminder --source=./functions/sendReminder/ --runtime=nodejs10 --trigger-http --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy upload_image --source=./functions/upload_image/ --runtime=python37 --trigger-http --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy recommendation --source=./functions/recommendation/ --runtime=nodejs10 --trigger-http