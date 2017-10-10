# synse-server-grpc
The internal GRPC API for Synse Server and its plugins


This repo serves as a central location for the Synse Server internal GRPC API
specification. Since we use a python client in Synse Server (2.0+) and a Go
server (in the plugins if using the Synse Plugin SDK), we need a common place
for this that is accessible to all.


TODO -- there is still a bit of work to be done here, especially around how things
are packaged up and used by the aforementioned components. will need to get things
up here properly so we can import via go and package up the python stuff so we can
install via pip.

Will also need to finalize this API. While I have had success with the Read and 
Metainfo commands, there is still design work/proving out of the Write and Transaction 
Check commands.