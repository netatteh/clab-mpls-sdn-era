# Containerlab topology for MPLS in the SDN Era

Containerlab topology description used to deploy the example topology defined in book [MPLS in the SDN era](https://www.oreilly.com/library/view/mpls-in-the/9781491905449/). The lab is built utilizing the Juniper cRPD image. Running the topology using a containerized NOS allows for a much smaller resource requirements than running VMs, and as such is great for labbing.

## Prerequisites

- License  and software image for cRPD. At the time of this writing, a 90 day trial license is available through Juniper support.

- Working [Containerlab](https://containerlab.dev) environment with Sudo access

- Python >3.6

## Installation

1. Clone this repository

2. Create and activate a new Python virtual environment to your desired location

```bash
python -m venv ~/.venv/clab-mpls-sdn-era
source ~/.venv/clab-mpls-sdn-era/bin/activate
```
3. Change directory in the repository folder and install the required dependencies

```bash
pip install -r requirements.txt
```

4. If using the evaluation cRPD image, download the .tgz package and load the image to your Docker environment

 ```bash
 docker load -i junos-routing-crpd-docker-19.4R1.10.tgz
 ```

5. Retrieve the cRPD license file from Juniper, and copy it to the base directory named as `crpd_license.txt`

6. Run `sudo make all`

7. When done, run `sudo make destroy`

## Notes

- The Makefile creates three Linux bridges to be used within the Containerlab topology. If the naming collides with your existing bridges, change the file accordingly.
- The 19.X software does not support MPLS features such as LDP, and therefore is not usable in this lab.
