deploy:
	brctl addbr br-pe-bridge
	brctl addbr h1-ce-bridge
	brctl addbr h3-br-bridge
	ifconfig br-pe-bridge up
	ifconfig h1-ce-bridge up
	ifconfig h3-br-bridge up
	containerlab deploy

destroy:
	containerlab destroy --cleanup
	ifconfig br-pe-bridge down
	ifconfig h1-ce-bridge down
	ifconfig h3-br-bridge down
	brctl delbr br-pe-bridge
	brctl delbr h1-ce-bridge
	brctl delbr h3-br-bridge

reconfigure:
	containerlab deploy --reconfigure

license:
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py pe1,pe2,pe3,pe4,rr1,rr2,p1,p2,ce1,ce2,br3,br4 pe --license ./crpd_license.txt

startup:
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py pe1,pe2,pe3,pe4 pe
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py rr1,rr2 rr
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py p1,p2 p
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py ce1,ce2 ce
	/home/attehelenius/.venv/clab-mpls-sdn-era/bin/python3 configure_lab.py br3,br4 br

all: deploy startup reconfigure license
