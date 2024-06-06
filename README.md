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
git clone https://github.com/idanshimon/kube-config-merge.git
cd kube-config-merge
pip install -r requirements.txt
```

## Usage
Run the script with the appropriate arguments:

### Merge a new configuration file:
```bash
$ python kmerge.py --merge /path/to/new/config.yaml
Backup of the original configuration has been saved to /home/user/.kube/config.bak
Merged configurations from /path/to/new/config.yaml
Configuration saved to /home/user/.kube/config
```
### Delete a specific cluster:

```bash
$ python kmerge.py --delete-cluster cluster-name
Backup of the original configuration has been saved to /home/user/.kube/config.bak
Deleted cluster cluster-name
Configuration saved to /home/user/.kube/config

```

### Delete a specific user:
```bash
$ python kmerge.py --delete-user username
Backup of the original configuration has been saved to /home/user/.kube/config.bak
Deleted user username
Configuration saved to /home/user/.kube/config

```

### List all users:
```bash
$ python kmerge.py --list-users
Users in the Kubernetes config:
user1
user2
user3

```

### List all contexts:
```bash
$ python kmerge.py --list-contexts
Contexts in the Kubernetes config:
context1
context2
context3

```

### List all clusters:
```bash
$ python kmerge.py --list-clusters
Clusters in the Kubernetes config:
cluster1
cluster2
cluster3

```

---

Thank you for using `kmerge`! If you have any questions, feedback, or contributions, feel free to reach out or open an issue on GitHub. Happy managing!
