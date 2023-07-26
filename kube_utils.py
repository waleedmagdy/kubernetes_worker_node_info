import re
from kubernetes import client, config 

def authenticate_with_kubernetes():
    config.load_kube_config()

def extract_node_name(node_name):
    # Regular expression pattern to extract the node name
    # The pattern looks for any substring starting with "Node: " and followed by any characters
    match = re.search(r"Node: (.+)", node_name)
    if match:
        return match.group(1)
    else:
        return node_name

def convert_ki_to_gb(kibibytes):
    kibibytes = kibibytes.strip().lower()
    if kibibytes.endswith('ki'):
        kibibytes = kibibytes[:-2]
    return round(int(kibibytes) / (1024 * 1024), 2)

def get_worker_nodes_info():
    v1 = client.CoreV1Api()
    nodes = v1.list_node().items

    worker_nodes_info = []

    for node in nodes:
        node_name = node.metadata.name
        cpu_capacity = node.status.capacity.get('cpu', 'N/A')
        memory_capacity_ki = node.status.capacity.get('memory', 'N/A')
        memory_capacity_gb = convert_ki_to_gb(memory_capacity_ki)
        storage_capacity = node.status.capacity.get('storage', 'N/A')

        node_name = extract_node_name(node_name)

        worker_nodes_info.append({
            'node_name': node_name,
            'cpu_capacity': cpu_capacity,
            'memory_capacity': memory_capacity_gb,
            'storage_capacity': storage_capacity,
        })

    return worker_nodes_info

def get_pods_running_on_nodes():
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces().items

    pods_running_on_nodes = {}

    for pod in pods:
        if pod.spec.node_name:
            node_name = pod.spec.node_name
            if node_name not in pods_running_on_nodes:
                pods_running_on_nodes[node_name] = 1
            else:
                pods_running_on_nodes[node_name] += 1

    return pods_running_on_nodes
