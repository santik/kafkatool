import os
import sqlite3


def create_db():
    create_tables = "CREATE TABLE configuration (clusterName PRIMARY KEY, zookeeperHost, zookeeperPort)"
    run_query(create_tables)
    default_local_configuration()

def default_local_configuration():
    insert_configuration("local", "localhost", "9092")

def run_query(sql, data=None, receive=False):
    conn = sqlite3.connect("db/configuration.db")
    cursor = conn.cursor()
    if data:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    if receive:
        return cursor.fetchall()
    else:
        conn.commit()

    conn.close()


def get_cluster(cluster_name):
    get_specific_cluster = "SELECT * FROM configuration WHERE clusterName = ?"
    return run_query(get_specific_cluster, (cluster_name,), True)


def get_all_clusters():
    get_all_clusters_sql = "SELECT clusterName FROM configuration"
    return run_query(get_all_clusters_sql, None, True)


def insert_configuration(cluster_name, zookeeper_host, zookeeper_port):
    insert_configuration_sql = "INSERT INTO configuration (clusterName, zookeeperHost, zookeeperPort) VALUES (?, ?, ?)"
    run_query(insert_configuration_sql, (cluster_name, zookeeper_host, zookeeper_port))


def update_configuration(cluster_name, zookeeper_host, zookeeper_port, old_cluster_name):
    update_configuration_sql = "UPDATE configuration set clusterName = ? , zookeeperHost = ?, zookeeperPort = ? WHERE clusterName = ?"
    run_query(update_configuration_sql, (cluster_name, zookeeper_host, zookeeper_port, old_cluster_name))


def delete_configuration(cluster_name):
    delete_configuration_sql = "DELETE FROM configuration WHERE clusterName = ?"
    run_query(delete_configuration_sql, (cluster_name,))


if not os.path.isfile("db/configuration.db"):
    print("Configuration table doesn't exists. Creating a new one.")
    create_db();