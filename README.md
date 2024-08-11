# MLOps Project for Pima Diabetes Prediction

This project is part of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/).

The dataset used in this project was sourced from [Kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database). Preliminary data analysis was conducted (see the [notebooks](/nbs) folder) to gain insights and guide further development.

## Problem Statement: Predicting Diabetes Risk in Patients

### Background

Diabetes is a major health concern globally, including among the Pima Indian population. The Pima Indians Diabetes Database contains medical and demographic data that can be used to predict the likelihood of diabetes in individuals. Developing an accurate predictive model could enable healthcare professionals to identify high-risk patients and intervene early, potentially improving health outcomes.

### Objective

The objective of this project is to develop a predictive model that assesses the risk of diabetes in Pima Indian women based on their health metrics. The model should predict the likelihood of diabetes given an individual's medical and demographic information. This project follows a systematic approach, beginning with data exploration and analysis, and culminating in the deployment and monitoring of a fully automated machine learning pipeline.

The pipeline is built using a combination of the following technologies:

- **Terraform**: Infrastructure provisioning
- **MageAI**: Workflow orchestration
- **MLflow**: Experiment tracking and model management
- **Evidently**: Model performance monitoring
- **Grafana**: Visualization
- **Hyperopt**: Hyperparameter optimization

## Technologies Used

- **Python**
- **Terraform**
- **AWS** (Kinesis, S3, EC2, ECR)
- **Docker**
- **Jupyter**
- **Pipenv/Pyenv**
- **Scikit-learn**
- **XGBoost**
- **MLflow**
- **Evidently**
- **Grafana**
- **Mage AI**
- **Hyperopt**
- **Pytest**
- **Pre-commit** (black, flake8)

## Project Workflow

### 1. Data Exploration and Analysis

The project begins with data exploration and preliminary analysis using Jupyter notebooks, which includes:

- **Loading and Inspecting the Data**: Using Jupyter to load the Pima Indians Diabetes dataset and examine its structure.
- **Exploratory Data Analysis (EDA)**: Understanding data distribution, identifying patterns, and detecting anomalies or missing values. This step includes:
  - Visualizing the distribution of features and target variables
  - Analyzing correlations between features
  - Identifying and handling missing or outlier data points
- **Feature Engineering**: Creating new features or transforming existing ones to improve model performance.

### 2. Building and Orchestrating the Pipeline

Following data exploration and preprocessing, the next phase involves building an automated machine learning pipeline. This pipeline is designed to be modular, scalable, and easily deployable across various environments.

- **Model Testing, Registry, and Deployment**: Using MLflow and MageAI for testing, model registry, and deployment.
- **Model Monitoring**: Implementing monitoring with Grafana and Evidently.
- **Infrastructure Setup**: Utilizing Terraform to provision project infrastructure on AWS, including Kinesis Streams (Producer & Consumer), Lambda (Serving API), S3 Bucket (Model artifacts), and ECR (Image Registry).

These services are accessible via assigned ports on the EC2 instance's DNS.

### 3. Continuous Integration and Continuous Deployment (CI/CD)

CI/CD practices are applied to automate testing and deployment, ensuring the project is robust and maintainable.

## Project Setup

### Prerequisites

1. **AWS IAM User**: Create a Terraform IAM user for infrastructure provisioning on AWS.
2. **S3 Bucket**: Create an S3 bucket named **tf-state-bucket-3** in the **eu-west-2** AWS region.

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Dakini/MLops_project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd MLops_project
   ```

3. Create a virtual environment using Pipenv:

   ```bash
   pip install pipenv
   pipenv shell
   ```

4. Install dependencies:

   ```bash
   make setup
   ```

5. Deploy infrastructure using Terraform:
   ```bash
   cd infrastructure
   terraform init
   terraform plan -var-file=vars/stg.tfvars
   terraform apply -var-file=vars/stg.tfvars
   ```

### Accessing Services

After Terraform completes the infrastructure provisioning, it will output variables such as the EC2 DNS and public IP. You can SSH into the EC2 instance using the following command:

```bash
ssh -i ssh-key.pem ec2-user@<YOUR EC2 IP ADDRESS>
```

You can access the following services via a web browser:

- **Mage AI**: Accessible at `http://<ec2PublicDNS>:6789`.

  - To initiate the data-ingestion pipeline, navigate to the "Pipelines" section, select "data-ingestion," and trigger it with the `@run-once` option. This pipeline will handle data ingestion, transformation, MLflow experiment tracking, model registration, and more.

  ![Mage AI Pipeline](image.png)

  - The pipeline also includes Hyperopt parameter tuning for XGBoost models and exports predictions to a PostgreSQL database, enabling Grafana to generate relevant plots. Evidently is used to explore statistics related to the dataset. You can explore and modify the pipeline's code directly through the Mage AI service, or by accessing the local code [here](/orchestration/prima-diabetes).

  ![Mage AI Pipeline Overview](image-1.png)

- **MLflow**: Accessible at `http://<ec2PublicDNS>:5002`. This service provides a comprehensive view of the experiments that have been run, along with the registered models. You can view the experiments and model aliases through the MLflow interface.

  ![MLflow Experiments](image-3.png)
  ![MLflow Models](image-4.png)

- **Grafana**: Accessible at `http://<ec2PublicDNS>:3000`. Grafana offers a basic dashboard displaying statistics on model predictions for both training and testing datasets. The default login credentials are:

  - **Username**: admin
  - **Password**: admin

  ![Grafana Dashboard](image-5.png)

### Testing

Run the integration test:

```bash
cd ..
make integration_test
```

### Kinesis Stream Test

Test the Kinesis Stream:

```bash
export KINESIS_STREAM_INPUT=input-kinesis-steam-prima-diabetes
aws kinesis put-record \
--stream-name ${KINESIS_STREAM_INPUT} \
--partition-key 1 --cli-binary-format raw-in-base64-out \
--data '{
\"data\": {
\"Pregnancies\": 0,
\"Glucose\": 131,
\"BloodPressure\": 0,
\"SkinThickness\": 0,
\"Insulin\": 0,
\"BMI\": 43.2,
\"DiabetesPedigreeFunction\": 0.27,
\"Age\": 26
},
\"patient_id\": \"256\"
}'
```

### Destroying Infrastructure

To tear down the infrastructure:

```bash
cd infrastructure
terraform destroy -var-file=vars/stg.tfvars 6. Create the virtual environment using pipenv:
```

9. Explore the services.
   After terraform has completed its creation of the relevant services. It will output some variables including the ec2 DNS and ec2 public ip.
   It is possible to ssh into the ec2 using the following command

   ```bash
   ssh -i ssh-key.pem ec2-user@<YOUR EC2 IP ADDRESS>
   ```

   It is also possible to view the services for the Grafana, MLFlow and Mage AI. In your web browser. I encourage you to use the mage service first, so that it can fill the MLflow, and grafana service too.

- Mage AI
  If you go to the ec2PublicDNS:6789, you will find the service.
  ![alt text](image.png)
  Where if you go to pipelines, open the data-ingestion and use the @run-once trigger it will run the pipeline.
  ![alt text](image-1.png)

  The pipeline includes, data ingestion, transforming of data, MlFlow experiment tracking and registration of models for the Lambda function. It also explores hyperopt parameter tuning of XGBoost Models. It also exports the predictions to a postgres database so that Grafana can provide some plts. Evidently is also used to explore some of the stats regarding the dataset. The code can be explored on the service, by editing the pipeline or visiting the local code [here](/orchestration/prima-diabetes).

  ![alt text](image-2.png)

- MLFlow
  This shows the experiments that have been run, and the alias of the models that have been registerd from the run. If you go to the ec2PublicDNS:5002, you will find the service.
  ![alt text](image-3.png)
  ![alt text](image-4.png)

- Grafana
  This service provides a basic dashboard with some stats regarding the predictions from the model on the training and testing set.
  If you go to the ec2PublicDNS:3000, you will find the service. Login is username: admin, password: admin.
  ![alt text](image-5.png)

6. Execute the integration test

   ```bash
   cd ..
   make integration_test
   ```

7. Test a kinesis Stream

   ```bash
   export KINESIS_STREAM_INPUT=input-kinesis-steam-prima-diabetes
   aws kinesis put-record \
   --stream-name ${KINESIS_STREAM_INPUT} \
   --partition-key 1 --cli-binary-format raw-in-base64-out \
   --data '{
   "data": {
   "Pregnancies": 0,
   "Glucose": 131,
   "BloodPressure": 0,
   "SkinThickness": 0,
   "Insulin": 0,
   "BMI": 43.2,
   "DiabetesPedigreeFunction": 0.27,
   "Age": 26
   },
   "patient_id": "256"
   }'
   ```

8. Destroy infrastruction

```bash
   cd infrastructure
   terraform destroy -var-file=vars/stg.tfvars
```

## Project Best Practices

The following best practices were implemented:

- :white_check_mark: **Problem description**: The project is well described and it's clear and understandable
- :white_check_mark: **Cloud**: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
- :white_check_mark: **Experiment tracking and model registry**: Both experiment tracking and model registry are used
- :white_check_mark: **Workflow orchestration**: Fully deployed workflow
- :white_check_mark: **Model deployment**: The model deployment code is containerized and can be deployed to the cloud
- :white_check_mark: **Model monitoring**: Basic model monitoring that calculates and reports metrics
- :white_check_mark: **Reproducibility**: Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified.
- :white_check_mark:**Best practices**:
  - [x] There are unit tests
  - [x] There is an integration test
  - [x] Linter and code formatting are used
  - [x] There is a Makefile
  - [x] There is a CI/CD pipeline
