deploy:
	brctl addbr br-pe-bridge
	brctl addbr h1-ce-bridge
	brctl addbr h3-br-bridge
	containerlab deploy

destroy:
	containerlab destroy
	brctl delbr br-pe-bridge
	brctl delbr h1-ce-bridge
	brctl delbr h3-br-bridge

configure:
	containerlab config -t mpls_sdn_era.clab.yml  template -p . -l core -f pe1,pe2,pe3,pe4,p1,p2,rr1,rr