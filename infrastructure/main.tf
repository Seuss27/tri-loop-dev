provider "aws" {
  region = var.aws_region
}

# ---------------------------------------------------------
# 1. Container Registry (ECR)
# ---------------------------------------------------------
resource "aws_ecr_repository" "agent_repo" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ---------------------------------------------------------
# 2. State Persistence (RDS PostgreSQL)
# LangGraph MemorySaver requires a DB to pause/resume graphs
# ---------------------------------------------------------
resource "aws_db_instance" "langgraph_state" {
  identifier             = "${var.project_name}-state-db"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t4g.micro" # Graviton processor (cheaper/faster)
  username               = var.db_username
  password               = var.db_password
  skip_final_snapshot    = true           # Set to false for production
  publicly_accessible    = false
}

# ---------------------------------------------------------
# 3. Compute Execution (ECS Fargate)
# ---------------------------------------------------------
resource "aws_ecs_cluster" "agent_cluster" {
  name = "${var.project_name}-cluster"
}

# IAM Role for Fargate to execute and pull images
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# The blueprint for your agent's container
resource "aws_ecs_task_definition" "agent_task" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"  # Adjust based on agent data processing needs
  memory                   = "1024" # 1GB RAM
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "tri-loop-backend"
    image     = "${aws_ecr_repository.agent_repo.repository_url}:latest"
    essential = true
    
    # Passing the DB URL so LangGraph knows where to save the state
    environment = [
      { name = "ENVIRONMENT", value = "production" },
      { name = "CHECKPOINT_DB_URL", value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.langgraph_state.endpoint}/${aws_db_instance.langgraph_state.db_name}" }
    ]
    
    # NOTE: LLM API Keys (Anthropic/OpenAI) should be passed securely via AWS Secrets Manager, 
    # not plaintext environment variables, in a full production setup.
  }])
}

# The service that keeps the container running
resource "aws_ecs_service" "agent_service" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.agent_cluster.id
  task_definition = aws_ecs_task_definition.agent_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1 # Keep at 1 for cost management; scale up if handling multiple users

  network_configuration {
    subnets          = ["subnet-xxxxxx", "subnet-yyyyyy"] # Replace with your default VPC subnets
    assign_public_ip = true
  }
}