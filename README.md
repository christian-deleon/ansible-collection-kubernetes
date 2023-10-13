# Ansible Collection - christian_deleon.kubernetes

## Usage

```yaml
---
- name: Configure Kubernetes
  hosts: cluster
  become: true
  roles:
    - role: christian_deleon.kubernetes.kubernetes
      tags: kubernetes

- name: Configure for NFS
  hosts: cluster
  become: true
  gather_facts: false
  roles:
    - role: christian_deleon.kubernetes.nfs_configure
      tags: kubernetes

- name: Install Helm
  hosts: controlplane_master
  become: true
  gather_facts: false
  roles:
    - role: christian_deleon.kubernetes.helm
      tags: kubernetes

- name: Configure Kubeconfig
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    kubeconfig_dir: /home/cdeleon/.kube
  roles:
    - role: christian_deleon.kubernetes.kubeconfig
      tags: kubernetes

- name: Configure Velero
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    velero_bucket: "velero-backup" # Name of the bucket to store backups in
  roles:
    - role: christian_deleon.kubernetes.velero
      tags: velero

- name: Configure Supporting Services
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    nfs_server: 192.168.1.27 # IP of the NFS server
    nfs_path: /mnt/Kubernetes # Path to the NFS share
    ip_range_lower_limit: 192.168.1.11
    ip_range_upper_limit: 192.168.1.15
  roles:
    - role: christian_deleon.kubernetes.nfs_provisioner
      tags: service

    - role: christian_deleon.kubernetes.metallb
      tags: service

    - role: christian_deleon.kubernetes.traefik
      tags: service

    - role: christian_deleon.kubernetes.argocd
      tags: service

    - role: christian_deleon.kubernetes.monitoring
      tags: service
```
