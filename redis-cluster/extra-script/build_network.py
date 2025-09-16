
import pulumi
import pulumi_aws as aws

cfg = pulumi.Config()
network_stack = cfg.require('networkStack')
net = pulumi.StackReference(network_stack)

vpc_id = net.get_output('vpc_id')
private_subnet_ids = net.get_output('private_subnet_ids')

redis_sg = aws.ec2.SecurityGroup(
    'redis-sg',
    vpc_id=vpc_id.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol='tcp', from_port=6379, to_port=6379,
        # TODO: tighten the app's SG instead of VPC-side access
        cidr_blocs=['10.0.0.0/16'],
    )],
    engress=[aws.ec2.SecurityGroupEngressArgs(
        protocol='-1', from_port=0, to_port=0, cidr_blocks=['0.0.0.0/0']
    )],
)

subnet_group = aws.elasticache.SubnetGroup(
    'redis-subnets',
    subnet_ids=private_subnet_ids,
    description='Private subnets for Redis',
)


rg = aws.elasticache.ReplicationGroup(
    'app-redis',
    replication_group_id='app-redis',
    engine='redis',
    node_type='cache.t4g.micro',
    subnet_group_name=subnet_group.name,
    security_group_ids=[redis_sg.id],
    port=6379,
)

pulumi.export('redis_primary_endpoint', rg.primary_endpoint_address)
pulumi.export('redis_reader_endpoint', rg.reader_endpoint_address)

