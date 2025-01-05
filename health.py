import boto3
import json
import sys
import subprocess

def get_active_aws_health_region():
    """
    Retrieve the active AWS Health API region by resolving the global.health.amazonaws.com CNAME.

    Returns:
        str: The active region endpoint (e.g., 'health.us-east-1.amazonaws.com') or None if unsuccessful.
    """
    try:
        result = subprocess.run(
            ["dig", "global.health.amazonaws.com", "+short"],
            capture_output=True,
            text=True
        )
        
        # Extract the CNAME from the output
        for line in result.stdout.splitlines():
            if line.endswith(".amazonaws.com."):
                active_endpoint = str(line.strip().split(".")[1])
                return active_endpoint

    except Exception as e:
        print(f"Error retrieving active AWS Health region: {e}")
    
    return None

def get_aws_health_events(services, event_status_codes, regions):
    """
    Fetch AWS Health events based on filter criteria and return a JSON object suitable for Terraform Data block.

    Parameters:
        services (list): List of AWS services to filter (e.g., ["EC2"]).
        event_status_codes (list): List of event statuses (e.g., ["open", "upcoming"]).
        regions (list): List of regions to filter (e.g., ["eu-north-1"]).

    Returns:
        dict: JSON object containing the events as a string.
    """
    # Create a Boto3 Health client
    active_aws_health_region = get_active_aws_health_region()
    health_client = boto3.client('health', region_name=active_aws_health_region)

    # Define the filter criteria
    filter_criteria = {
        "services": services,
        "eventStatusCodes": event_status_codes,
        "regions": regions
    }

    try:
        # Call the AWS Health DescribeEvents API
        response = health_client.describe_events(
            filter=filter_criteria
        )

        # Extract only the events
        events = response.get("events", [])
        return {"events": json.dumps(events), "active_aws_health_region": active_aws_health_region}

    except health_client.exceptions.SubscriptionRequiredException as e:
        return {"error": "A Business or Enterprise Support plan is required."}

    except Exception as e:
        return {"error": "An unexpected error occurred."}


if __name__ == "__main__":
    # Parse input from Terraform
    input_params = json.load(sys.stdin)
    services = input_params.get("services", "").split(",")
    event_status_codes = ["open", "upcoming"]  # Fixed as per original request
    regions = input_params.get("regions", "").split(",")

    result = get_aws_health_events(services, event_status_codes, regions)

    print(json.dumps(result))