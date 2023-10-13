# Kubernetes NFS Provisioner

## Variables

- `nfs_server_ip`: IP address of the NFS server
- `nfs_server_path`: Path to the NFS share
- `nfs_provisioner_name`: Name of the provisioner (default: nfs-provisioner)
- `nfs_namespace`: Namespace to deploy the provisioner (default: nfs)
- `nfs_storage_class_name`: Name of the storage class (default: nfs)
- `nfs_reclaim_policy`: Reclaim policy for the storage class (default: Retain - other options: Delete)
- `nfs_default_class`: Set the storage class as the default (default: true)
