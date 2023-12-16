# Ansible Collection - christian_deleon.kubernetes

## RKE2 example playbook

```yaml
---
- name: Configure Kubernetes
  hosts: cluster
  become: true

  roles:
    - role: christian_deleon.kubernetes.rke2
      tags: rke2

- name: Configure kubeconfig
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    kubeconfig_name: "{{ context_name }}"

  roles:
    - role: christian_deleon.kubernetes.kubeconfig
      tags: kubeconfig
```

## Kubeadm example playbook

```yaml
---
- name: Configure Kubernetes
  hosts: cluster
  become: true
  
  roles:
    - role: christian_deleon.kubernetes.kubeadm
      tags: kubeadm

- name: Configure for NFS
  hosts: cluster
  become: true
  gather_facts: false
  
  roles:
    - role: christian_deleon.kubernetes.nfs_configure
      tags: nfs

- name: Install Helm
  hosts: controlplane_master
  become: true
  gather_facts: false
  
  roles:
    - role: christian_deleon.kubernetes.helm
      tags: helm

- name: Configure Kubeconfig
  hosts: localhost
  connection: local
  gather_facts: false
  
  vars:
    kubeconfig_name: "{{ context_name }}"
  
  roles:
    - role: christian_deleon.kubernetes.kubeconfig
      tags: kubeconfig

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
    nfs_server: nfs.example.com # Hostname or IP of the NFS server
    nfs_path: /mnt/nfs # Path to the NFS share
    ip_range_lower_limit: 192.168.1.11 # Lower limit of the IP range for MetalLB
    ip_range_upper_limit: 192.168.1.15 # Upper limit of the IP range for MetalLB
  
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
