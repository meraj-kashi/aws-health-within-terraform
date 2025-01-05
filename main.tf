# Terraform external data block
data "external" "radlands" {
  program = ["python3", "./health.py"]

  query = {
    services = "S3"
    regions  = "eu-north-1,eu-west-1"
  }
}

# Terraform s3 bucket - conditional creation
resource "aws_s3_bucket" "radlands" {
  bucket = "cloudynotes-io-radlands"

  lifecycle {
    precondition {
      condition     = data.external.radlands.result.events == jsonencode([])
      error_message = "Service health check failed: ${data.external.radlands.query.services} are not in a healthy state."
    }
  }
}

# Output health_events and active_endpoint
output "health_events" {
  value = data.external.radlands.result.events
}

output "health_active_endpoint" {
  value = data.external.radlands.result.active_aws_health_region
}
