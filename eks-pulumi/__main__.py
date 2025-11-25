"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
# import pulumi_aws.eks as eks
import pulumi_eks as eks


config = pulumi.Config()
desired_capacity = config.get_int("desiredCapacity") or 2
min_size = config.get_int("minSize") or 1
max_size = config.get_int("maxSize") or 3
instance_type = config.get("instanceType") or "t2.micro"
cluster_version = config.get("clusterVersion") or "1.30"
region = aws.config.region or "us-west-2"


# --- VPC ---
vpc = aws.ec2.Vpc(
    "eks-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "eks-vpc"}
)

igw = aws.ec2.InternetGateway("eks-igw", vpc_id=vpc.id)


# -- Public subnets ---
public_subnet_1 = aws.ec2.Subnet(
    "eks-public-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    availability_zone=f'{region}a',
    tags={"Name": "eks-public-1"}
)

public_subnet_2 = aws.ec2.Subnet(
    "eks-public-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=True,
    availability_zone=f'{region}b',
    tags={"Name": "eks-public-2"}
)

route_table = aws.ec2.RouteTable(
    "eks-public-rt",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igw.id
        )
    ],
)

aws.ec2.RouteTableAssociation(
    "eks-rta-1",
    subnet_id=public_subnet_1.id,
    route_table_id=route_table.id
)

aws.ec2.RouteTableAssociation(
    "eks-rta-2",
    subnet_id=public_subnet_2.id,
    route_table_id=route_table.id
)


# --- EKS ---
cluster = eks.Cluster(
    "demo-eks",
    version=cluster_version,
    vpc_id=vpc.id,
    subnet_ids=[public_subnet_1.id, public_subnet_2.id],
    instance_type=instance_type,
    desired_capacity=desired_capacity,
    min_size=min_size,
    max_size=max_size,
    node_associate_public_ip_address=True,
    create_oidc_provider=True
)


#  --- Outputs ---
pulumi.export("VpcId", vpc.id)
pulumi.export("subnetIds", pulumi.Output.all(public_subnet_1.id, public_subnet_2.id))
pulumi.export("kubeconfig", cluster.kubeconfig)
pulumi.export("clusterName", cluster.core.cluster.name)

