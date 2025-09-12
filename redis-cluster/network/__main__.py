import pulumi, pulumi_aws as aws

vpc = aws.ec2.Vpc('app-vpc', cidr_block='10.0.0.0/16',
                  enable_dns_support=True,
                  enable_dns_hostnames=True
                  )

azs = aws.get_availability_zones(state='available').names[:2]
privates = []

for i, azs in enumerate(azs):
    s = aws.ec2.Subnet(f'private-{i+1}',
                       vpc_id=vpc.id,
                       cidr_block=f'10.0.{100+i}.0/24',
                       availability_zones=azs,
                       map_public_ip_launch=False)
    privates.append(s)

pulumi.export('vpc_id', vpc.id)
pulumi.export('private_subnet_ids', [s.id for s in privates])

