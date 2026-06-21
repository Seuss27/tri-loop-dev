output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.agent_repo.repository_url
}

output "database_endpoint" {
  description = "The connection endpoint for the PostgreSQL state database"
  value       = aws_db_instance.langgraph_state.endpoint
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.agent_cluster.name
}