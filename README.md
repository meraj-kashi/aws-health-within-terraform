# Plan for Unsuccessful Changes; A Use Case of the AWS Health API

This is a code example demonstrating how to use the AWS Health API to check the status of services before deploying resources. The health check is integrated into a Terraform configuration using the external data block and the precondition lifecycle.

> To access the AWS Health API, your account must be subscribed to a Business, Enterprise On-Ramp, or Enterprise Support plan from AWS Support. If you attempt to call the AWS Health API from an account without one of these support plans, you will encounter a `SubscriptionRequiredException` error.

For more information and detailed explanations, please visit my blog post: https://cloudynotes.io/blog/radlands.html