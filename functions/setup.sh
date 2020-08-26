echo "y" | gcloud functions deploy automl --source=./automl/ --runtime=python37 --trigger-topic=new-product --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy detect_labels --source=./detect_labels/ --runtime=python37 --trigger-topic=new-product --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy pay_with_stripe --source=./pay_with_stripe/ --runtime=python37 --trigger-topic=payment-process --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy sendOrderConfirmation --source=./sendOrderConfirmation/ --runtime=nodejs10 --trigger-topic=payment-completion --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy sendReminder --source=./sendReminder/ --runtime=nodejs10 --trigger-http --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy streamEvents --source=./streamEvents/ --runtime=nodejs10 --trigger-http --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy upload_image --source=./upload_image/ --runtime=python37 --trigger-http --env-vars-file=./extras/cloudbuild/functions_env_vars.yaml
echo "y" | gcloud functions deploy recommendation --source=./recommendation/ --runtime=nodejs10 --trigger-http