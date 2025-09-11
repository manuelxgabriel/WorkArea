from aws_cdk import Stack, CfnOutput
from constructs import Construct
from aws_cdk import aws_ec2 as ec2


class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope,construct_id, **kwargs)

        # print(ec2.IpAddresses.cidr("10.0.0.0/16"))
        vpc = ec2.Vpc(
            self, "Vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=3,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-a", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=20
                )

            ],
            enable_dns_support=True,
            enable_dns_hostnames=True,
        )
        CfnOutput(self, "VpcId", value=vpc.vpc_id)
        CfnOutput(self, "PublicSubnets",
                  value=",".join([s.subnet_id for s in vpc.public_subnets])
                  )
        print("Vpc Created !")
