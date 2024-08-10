# Predict prima diabetes

'''bash
pipenv shell
make setup
'''

# Use Mlflow to track the experiments and hyperparameter tuning

# Run from AWS for training and experiment and model registry promotion

# Orchestrate with Mage or Prefect / Airflow

# Creaet Infrastructure from Terraform

# Create a Rest API or something

# Docker, Docker Compose and unit tests

export KINESIS_STREAM_INPUT=input-kinesis-steam-prima-diabetes
export KINESIS_STREAM_OUTPUT=output-kinesis-steam-prima-diabetes
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

SHARD='shardId-000000000001'

SHARD_ITERATOR=$(aws kinesis \
 get-shard-iterator \
 --shard-id ${SHARD} \
 --shard-iterator-type TRIM_HORIZON \
 --stream-name ${KINESIS_STREAM_INPUT} \
 --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode

aws kinesis get-shard-iterator \
 --stream-name $KINESIS_STREAM_INPUT \
 --shard-id $SHARD \
 --shard-iterator-type TRIM_HORIZON
