"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create the S3 bucket with tagging and force destroy
bucket = s3.Bucket('my-bucket',
                   force_destroy=True,
                   tags={
                       'Environment': 'dev',
                       'Owner': 'manuel',
                        }
                   )

# Block all public access
s3.BucketPublicAccessBlock('my-bucket-public-access',
                           bucket=bucket.id,
                           block_public_acls=True,
                           block_public_policy=True,
                           ignore_public_acls=True,
                           restrict_public_buckets=True
                           )

# Enable versioning
s3.BucketVersioningV2('my-bucket-versioning',
                      bucket=bucket.id,
                      versioning_configuration=s3.BucketVersioningV2VersioningConfigurationArgs(
                          status='Enabled'
                        )
                      )

# Enable AES256 encryption
s3.BucketServerSideEncryptionConfigurationV2('my-bucket-encryption',
                                             bucket=bucket.id,
                                             rules=[s3.BucketServerSideEncryptionConfigurationV2RuleArgs(
                                                 apply_server_side_encryption_by_default=s3.BucketServerSideEncryptionConfigurationV2RuleApplyServerSideEncryptionByDefaultArgs(
                                                     sse_algorithm='AES256'
                                                 )
                                             )]
                                             )

# Export bucket name and ARN
pulumi.export('bucket_name', bucket.id)
pulumi.export('bucket_arn', bucket.arn)

