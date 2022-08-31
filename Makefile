deploy:
	brctl addbr br-pe-bridge
	brctl addbr h1-ce-bridge
	brctl addbr h3-br-bridge
	containerlab deploy

destroy:
	containerlab destroy --cleanup
	brctl delbr br-pe-bridge
	brctl delbr h1-ce-bridge
	brctl delbr h3-br-bridge

reconfigure:
	containerlab deploy --reconfigure

startup:
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py pe1,pe2,pe3,pe4,p1,p2,rr1,rr2 core
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py ce1,ce2,br1,br2 empty

all: deploy startup reconfigure
