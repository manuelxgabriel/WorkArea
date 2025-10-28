import boto3
import json
import time


def send_command(command, comment):
    """Helper to send a SSM command and wait for completion"""
    region = "us-west-2"
    ssm = boto3.client("ssm")
    INSTANCE_ID = "i-081217a79c7d2f8fe"

    response = ssm.send_command(
        InstanceIds=[INSTANCE_ID],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [command]},
        Comment=comment
    )
    comment_id = response["Command"]["CommandId"]

    print(response)


def install_cloudwatch_agent():
    """Install CloudWatch Agent via SSM"""
    cmd = "sudo yum install -y amazon-cloudwatch-agent || sudo apt-get install -y amazon-cloudwatch-agent"
    send_command(cmd, "Install CloudWatch")


if __name__ == "__main__":
    install_cloudwatch_agent()