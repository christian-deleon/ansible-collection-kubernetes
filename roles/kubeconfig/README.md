# Kubernetes kubeconfig Role

This role will configure a kubeconfig file for a given context.

## Required Variables

| Variable | Description | Default | Example |
| -------- | ----------- | ------- | ------- |
| 'kubeconfig_env_file' | File to where you set KUBECONFIG environment variable | ~/.bashrc | |
| 'kubeconfig_dir' | Directory where kubeconfig file will be stored | ~/.kube | |
| 'kubeconfig_name' | Name of kubeconfig file | | my-config |
