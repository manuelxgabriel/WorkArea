"""An AWS Python Pulumi program

    Description:
    This is create is able to create a VPC with 3 public subnets.
"""

import pulumi
import pulumi_aws as aws

# ------ Settings ---------#
VPC_CIDR = '10.0.0.0/16'
PUBLIC_SUBNET_CIDRS = ['10.0.0.0/24', '10.0.1.0/24', '10.0.2.0/24']

# Get up to 3 availability zones in the current region
azs = aws.get_availability_zones(state='available').names[:3]

# --------- VPC -----------#
vpc = aws.ec2.Vpc(
    'app-vpc',
    cidr_block=VPC_CIDR,
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={'Name': 'app-vpc'},
)

# Internet Gateway for public subnets
igw = aws.ec2.InternetGateway(
    'app-igw',
    vpc_id=vpc.id,
    tags={
        'Name': 'app-igw'
    }
)

public_rt = aws.ec2.RouteTable(
    'app-public-rt',
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block='0.0.0.0/0',
            gateway_id=igw.id,
        ),
    ],
    tags={'Name': 'app-public-rt'}
)

# Create 3 public subnets (mapPublicOnLaunch=True) and associate to route table
public_subnets = []
for i, cidr in enumerate(PUBLIC_SUBNET_CIDRS):
    subnet = aws.ec2.Subnet(
        f'app-public-subnet-{i+1}',
        vpc_id=vpc.id,
        cidr_block=cidr,
        availability_zone=azs[i % len(azs)],
        map_public_ip_on_launch=True,
        tags={'Name': f'app-public-{i+1}'}
    )

    aws.ec2.RouteTableAssociation(
        f'app-public-rta-{i+1}',
        route_table_id=public_rt.id,
        subnet_id=subnet.id,
    )
    public_subnets.append(subnet)

pulumi.export('vpc_id', vpc.id)
pulumi.export('igw_id', igw.id)
pulumi.export('public_route_table_id', public_rt.id)
pulumi.export('public_subnet_ids', [s.id for s in public_subnets])
pulumi.export('public_subnet_azs', [s.availability_zone for s in public_subnets])

