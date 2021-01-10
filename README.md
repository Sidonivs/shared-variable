# shared-variable
Semestral project for Distributed Systems and Calculations course at FEE CTU.

## notes
Command to generate GRPC files (in the `src` dir):\
`python3 -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/shared_variable.proto`