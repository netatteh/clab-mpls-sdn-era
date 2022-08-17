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