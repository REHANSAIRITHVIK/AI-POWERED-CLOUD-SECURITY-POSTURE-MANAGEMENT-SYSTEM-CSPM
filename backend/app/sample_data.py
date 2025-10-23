# sample_data.py
# Example resource payloads you can send to /scan
SAMPLE_RESOURCES = [
    {
        "cloud_provider": "aws",
        "resource_type": "s3",
        "resource_id": "bucket-photos-public",
        "config": {"type":"s3", "acl":"public-read", "encryption":False, "versioning":False}
    },
    {
        "cloud_provider": "aws",
        "resource_type": "ec2",
        "resource_id": "web-server-1",
        "config": {"type":"vm", "open_ports":[22,80], "public_ip":True, "os":"linux"}
    },
    {
        "cloud_provider": "gcp",
        "resource_type": "storage",
        "resource_id": "gcp-bucket",
        "config": {"type":"storage","acl":"private", "encryption":True}
    },
    {
        "cloud_provider": "aws",
        "resource_type": "iam",
        "resource_id": "admin-policy",
        "config": {"policy":"*"}
    }
]
    