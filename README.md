# Shared Variable
Semestral project for Distributed Systems and Calculations course at FEE CTU.

## Instalation

1. GRPC: https://grpc.io/docs/languages/python/quickstart/
    - Works without issues in Windows 10.
    - In Debian I recommend using virtualenv.
2. PyYAML: `pip install pyyaml`
    - Use `pip3` if you also have python 2 installed.
    
## Execution

- Command line (terminal): `python src/node.py <nodeID>`
    - `<nodeID>` is the top level key in node_config.yaml
    - Use `python3` if you also have python 2 installed.
- IDE:
    - Script path: `/path/to/shared-variable/src/node.py`
    - Parameters: `<nodeID>`

## Description

- Topology: Ring
- Leader election algorithm: Chang-Roberts

The shared variable is stored in the leader node.\
Each node remembers information about it's next node, previous node, next next node and the leader.\
When a node dies the first other node that finds out about it will start a topology repair.
The topology repair can also be started manually with a corresponding command.
If the dead node was a leader a new leader will be elected. 
Nodes with the most up-to-date shared variable value will have a higher chance to be elected.\
A node can also leave the cluster properly by signaling it's previous node to repair the topology.\
The latest shared variable value is always stored in at least two nodes to avoid loosing it.\
If a node wants to join the cluster it needs to know at least one address of a node that is already in the cluster.

## Notes
Command to generate GRPC files (in the `src` dir):\
`python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/shared_variable.proto`