# kmerge

Kubernetes Configuration Manager

## Overview
This script helps manage Kubernetes configuration files (`kubeconfig` files) by providing functionalities to merge configurations, delete clusters or users, and list clusters, contexts, and users. The script also supports backing up the original configuration before making any changes.

## Features
- **Backup Configuration**: Automatically backs up the original configuration file.
- **Merge Configurations**: Merges a new configuration file into the existing one.
- **Delete Cluster**: Deletes a specified cluster from the configuration.
- **Delete User**: Deletes a specified user from the configuration.
- **List Users**: Lists all users in the configuration.
- **List Contexts**: Lists all contexts in the configuration.
- **List Clusters**: Lists all clusters in the configuration.

## Installation

Clone the repository and install the dependencies:
```sh
git clone hhttps://github.com/idanshimon/kube-config-merge.git
cd kube-config-merge
pip install -r requirements.txt
