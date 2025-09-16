"""
    Pulumi
"""

import pulumi
import pulumi_aws as aws

# Configure bits
cfg = pulumi.Config()
vpc_cidr = cfg.get('vpcCidr') or '10.0.0.0/16'
private_subnet_cidr = cfg.get_object('privateSubnetCidrs') or ['10.0.1.0/24', '10.0.2.0/24']

print(private_subnet_cidr)

# VPC
vpc = aws.ec2.Vpc(
    'main-vpc',
    cidr_block=vpc_cidr,
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={'Name': 'main-vpc'}
)

azs = aws.get_availability_zones(state='available').names[:2]

private_subnet = []
for i, cidr in enumerate(private_subnet_cidr):
    private_subnet.append(
        aws.ec2.Subnet(
            f'private-subnet-{i+1}',
            vpc_id=vpc.id,
            cidr_block=cidr,
            availability_zone=azs[i % len(azs)],
            map_public_ip_on_launch=False,
            tags={'Name': f'private-{i+1}'},
        )
    )


pulumi.export('vpc_id', vpc.id)
pulumi.export('vpc_cidr', vpc_cidr)
pulumi.export('private_subnet_ids', [s.id for s in private_subnet])
