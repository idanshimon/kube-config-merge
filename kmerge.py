#!/usr/bin/env python3

import argparse
import os
import shutil
import yaml
import sys

def backup_config(config_path):
    """
    Creates a backup of the original configuration file.

    Parameters:
    config_path (str): The path to the original configuration file.

    Returns:
    None
    """
    backup_path = config_path + '.bak'
    if not os.path.exists(backup_path):
        shutil.copyfile(config_path, backup_path)
        print(f"Backup of the original configuration has been saved to {backup_path}")

def load_config(config_path):
    """
    Loads the configuration file from the specified path.

    Parameters:
    config_path (str): The path to the configuration file.

    Returns:
    dict: The loaded configuration.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_config(config, config_path):
    """
    Saves the configuration to the specified path.

    Parameters:
    config (dict): The configuration data.
    config_path (str): The path to save the configuration file.

    Returns:
    None
    """
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    print(f"Configuration saved to {config_path}")

def merge_configs(existing_config, new_config_path):
    """
    Merges a new configuration file into the existing configuration.

    Parameters:
    existing_config (dict): The current configuration data.
    new_config_path (str): The path to the new configuration file to merge.

    Returns:
    dict: The merged configuration.
    """
    with open(new_config_path, 'r') as file:
        new_config = yaml.safe_load(file)
        changes_made = False
    for key in ['clusters', 'contexts', 'users']:
        if key in new_config:
            existing_names = {item['name'] for item in existing_config.get(key, [])}
            new_items = [item for item in new_config[key] if item['name'] not in existing_names]
            if new_items:
                existing_config[key] = existing_config.get(key, []) + new_items
                changes_made = True
    return existing_config, changes_made

def delete_cluster(config, cluster_name):
    """
    Deletes a specified cluster from the configuration.

    Parameters:
    config (dict): The current configuration data.
    cluster_name (str): The name of the cluster to delete.

    Returns:
    dict: The updated configuration without the specified cluster.
    """
    initial_count = len(config['clusters'])
    config['clusters'] = [cluster for cluster in config.get('clusters', []) if cluster['name'] != cluster_name]
    config['contexts'] = [context for context in config.get('contexts', []) if context['context']['cluster'] != cluster_name]
    config['users'] = [user for user in config.get('users', []) if user['name'] != cluster_name]
    if config.get('current-context', '') == cluster_name:
        config['current-context'] = ''
    return config, len(config['clusters']) != initial_count

def delete_user(config, username):
    """
    Deletes a specified user from the configuration.

    Parameters:
    config (dict): The current configuration data.
    username (str): The name of the user to delete.

    Returns:
    dict: The updated configuration without the specified user.
    """
    initial_count = len(config['users'])
    users = config.get('users', [])
    config['users'] = [user for user in users if user['name'] != username]
    return config, len(config['users']) != initial_count

def list_users(config):
    """
    Lists all users in the configuration.

    Parameters:
    config (dict): The current configuration data.

    Returns:
    list: A list of user names.
    """
    return [user['name'] for user in config.get('users', [])]

def list_contexts(config):
    """
    Lists all contexts in the configuration.

    Parameters:
    config (dict): The current configuration data.

    Returns:
    list: A list of context names.
    """
    return [context['name'] for context in config.get('contexts', [])]

def list_clusters(config):
    """
    Lists all clusters in the configuration.

    Parameters:
    config (dict): The current configuration data.

    Returns:
    list: A list of cluster names.
    """
    return [cluster['name'] for cluster in config.get('clusters', [])]

def main():
    """
    Main function that parses command-line arguments and performs the requested actions.

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description='Kubernetes Configuration Manager')
    parser.add_argument('-c', '--config', type=str, default=os.path.expanduser('~/.kube/config'), help='Path to the Kubernetes config file')
    parser.add_argument('-m', '--merge', metavar='NEW_CONFIG_PATH', type=str, help='Path to the new config to merge')
    parser.add_argument('-d', '--delete-cluster', metavar='CLUSTER_NAME', type=str, help='Name of the cluster to delete')
    parser.add_argument('-b', '--backup', action='store_true', help='Backup the original configuration')
    parser.add_argument('-lu', '--list-users', action='store_true', help='List all users from the Kubernetes config')
    parser.add_argument('-lc', '--list-contexts', action='store_true', help='List all contexts from the Kubernetes config')
    parser.add_argument('-lk', '--list-clusters', action='store_true', help='List all clusters from the Kubernetes config')
    parser.add_argument('-du', '--delete-user', metavar='USERNAME', type=str, help='Name of the user to delete from the Kubernetes config')
    args = parser.parse_args()

    if not (args.merge or args.delete_cluster or args.delete_user or args.list_users or args.list_contexts or args.list_clusters):
        parser.print_help()
        exit(1)

    if args.backup:
        backup_config(args.config)

    config = load_config(args.config)
    changes_made = False

    if args.merge:
        config, changed = merge_configs(config, args.merge)
        changes_made = changes_made or changed
        print(f"Merged configurations from {args.merge}")
    
    if args.delete_cluster:
        config, changed = delete_cluster(config, args.delete_cluster)
        changes_made = changes_made or changed
        print(f"Deleted cluster {args.delete_cluster}")

    if args.delete_user:
        config, changed = delete_user(config, args.delete_user)
        changes_made = changes_made or changed
        print(f"Deleted user {args.delete_user}")

    if args.list_users:
        users = list_users(config)
        print("Users in the Kubernetes config:")
        for user in users:
            print(user)

    if args.list_contexts:
        contexts = list_contexts(config)
        print("Contexts in the Kubernetes config:")
        for context in contexts:
            print(context)

    if args.list_clusters:
        clusters = list_clusters(config)
        print("Clusters in the Kubernetes config:")
        for cluster in clusters:
            print(cluster)

    if changes_made:
        save_config(config, args.config)

if __name__ == '__main__':
    main()
