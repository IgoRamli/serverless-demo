# Extracting Insights using BigQuery and Data Studio

One of the important aspects of an e-commerce application is analyzing sales and user data. For a popular store with high amounts of traffic each minute (which is simulated through our [load generator](LoadGenerator.md)), tools for processing huge amounts of data like BigQuery is necessary in order to extract insights from our sales data.

BigQuery allows developers to analyze datas efficiently. BigQuery offers on-demand queries and charge users based on their usage only. This makes BigQuery cost-efficient.

## Architecture

Serverless Store uses Firestore as it's transactional database. Firestore is a NoSQL type database, so transferring it to BigQuery - which is a RDBMS - requires some kind of adapter. Luckily, Firebase provides an extension which allows easy real-time transfer from Firestore to BigQuery.

## Set Up Guide

Although our BigQuery database is created automatically by Terraform, we still need to manage the extension manually. It is possible to just export Firestore content periodically to BigQuery. However, total mirroring like that is an expensive operation. Therefore, it is best to append new data each time there is a change in the database. This process is automated using Firebase's extension [Export Collections to BigQuery](https://firebase.google.com/products/extensions/firestore-bigquery-export).

### Step 1: Instlal Firebase Extension for Real-Time Update

- Create a BigQuery dataset called `sample_data` with table `sample_table` inside. If you have run Terraform from [the main set-up guide](../README.md), this resources whould have been provisioned to you. If you wish to create them manually, follow these steps:
  - Go to [BigQuery](https://console.cloud.google.com/bigquery) and click your project name on the left drawer.
  - Below the SQL editor, click **Create Dataset**.
  - Name the new dataset `sample_data` and click **Create Dataset**.
  - Click your newly made dataset, and click **Create Table**.
  - Name the new table `sample_table`.
  - In the **Schema** section, add these fields:
    - Name : eventType; Type: STRING; Mode: NULLABLE
    - Name : createdTime; Type: STRING; Mode: NULLABLE
    - Name : context; Type: STRING; Mode: NULLABLE
  - Click **Create Table**.
- Install [Export Collections to BigQuery](https://firebase.google.com/products/extensions/firestore-bigquery-export) to your Firebase project.
- Follow the installation steps.
- At the final step, you will be asked to **Configure extension**. Add these information:
  - Cloud Function location : Select the location closest to you
  - Collection path : orders
  - Dataset ID : sample_data
  - Table ID : sample_table
- Click **Install Extension**.
- Wait until the installation is finished.

After the installation is finished, go to BigQuery main page. You should see table `orders_raw_changelog` and view `orders_raw_latest` under dataset `sample_data`. If you wish to try out the real-time update feature of this extension, feel free to follow the tutorial given by Firebase when you click **Get Started** on the Extensions Page.

### Step 2: Backfill your Existing Collections

As stated by _Export Collections to BigQuery_ description, only collections update done after the extension is installed will be logged to BigQuery. To import all existing data in your Firebase collections, you need to perform a backfill explained [here](https://github.com/firebase/extensions/blob/master/firestore-bigquery-export/guides/IMPORT_EXISTING_DOCUMENTS.md).

### Step 3: Generate Schema

After your data is in BigQuery, you can use the schema-views script (provided by this extension) to create views that make it easier to query relevant data. You only need to provide a JSON schema file that describes your data structure, and the schema-views script will create the views.

Learn more about using the schema-views script to [generate schema views](https://github.com/firebase/extensions/blob/master/firestore-bigquery-export/guides/GENERATE_SCHEMA_VIEWS.md).
