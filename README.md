# Containerlab topology for MPLS in the SDN Era

Containerlab topology description used to deploy the example topology defined in book [MPLS in the SDN era](https://www.oreilly.com/library/view/mpls-in-the/9781491905449/). The lab is built utilizing the Juniper cRPD image.

## Prerequisites

- License for cRPD. At the time of this writing, a 90 day trial license is available through Juniper support.

- Working [Containerlab](https://containerlab.dev) environment with Sudo access

## Installation

1. Clone this repository

2. If using the evaluation cRPD image, download the .tgz package and load the image to your Docker environment

 ```bash
 docker load -i junos-routing-crpd-docker-19.4R1.10.tgz
 ```

3. Retrieve the cRPD license file from Juniper, and copy it to the base directory named as `crpd_license.txt`

4. Run `sudo make deploy`

5. When done, run `sudo make destroy`

## Notes

- The Makefile creates three Linux bridges to be used within the Containerlab topology. If the naming collides with your existing bridges, change the file accordingly.
