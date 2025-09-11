#!/usr/bin/env python3
"""
AWS CDK
Goal: A VPC with six public subnets (two per AZ across three AZs)
"""
import aws_cdk as cdk
from vpc_stack import VpcStack

curr_account = "975678946404"
region = 'us-west-2'


def main():
    app = cdk.App()
    VpcStack(app, "MyVpc",
             env=cdk.Environment(account=curr_account, region=region))
    app.synth()


if __name__ == "__main__":
    main()

