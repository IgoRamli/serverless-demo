# serverless-demo
Refactoring of Serverless Demo Application by Google

## How to Set Up

TODO: Revamp this guide!

- Set up AutoML model using images given in the /extra folder.
- Initialize Firebase byt creating a new project in the `console.firebase.google.com`.
- Set up Firestore with Native Mode
- Create a new Web App on Firebase, write down the firebase-config.json file, and save it into both frontend and backend folder
- Build each microservices separately using Cloud Build.
- Create Stripe account and write down the API Key.
- Insert environment variables (AutoML model ID, Stripe API Token, GCS Bucket) in functions_env_vars.yaml
- Run Terraform to generate the rest of resources.
- Add front end service's IP Address on Firebase Auth Authorized Domain