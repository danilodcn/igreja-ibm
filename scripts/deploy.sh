CONTAINER_NAME=454947002543.dkr.ecr.us-east-1.amazonaws.com/ibm-prod:latest
SERVICE_NAME=service-production
TASK_DEFINITION_NAME=td-ibm-prod-web
AWS_DEFAULT_REGION=us-east-1
CLUSTER_NAME=cluster-ibm

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $CONTAINER_NAME
docker build -t image .

docker tag image:latest $CONTAINER_NAME

docker push $CONTAINER_NAME

TASK_DEFINITION=$(aws ecs describe-task-definition --region $AWS_DEFAULT_REGION --task-definition "$TASK_DEFINITION_NAME")

NEW_CONTAINER_DEFINTIION=$(echo $TASK_DEFINITION | jq --arg IMAGE "$CONTAINER_NAME" '.taskDefinition.containerDefinitions[0].image = $IMAGE | .taskDefinition.containerDefinitions[0]')

echo $(aws ecs register-task-definition --region $AWS_DEFAULT_REGION --family "$TASK_DEFINITION_NAME"  --container-definitions "$NEW_CONTAINER_DEFINTIION" --requires-compatibilities=FARGATE --network-mode awsvpc --execution-role-arn arn:aws:iam::454947002543:role/ecsTaskExecutionRole --cpu 256 --memory 512)

echo $(aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --task-definition $TASK_DEFINITION_NAME)