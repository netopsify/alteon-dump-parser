# alteon-dump-parser

This is a simple parser for Alteon Loadbalancer state dump.
This uses Ansible Engine and it parser functionality.

You will provide Alteon's device state dump as input as `radware.txt`. (The name can be changed in the playbook).
It will then generate a YAML file `radware.yml` with the extracted data.
It will also generate a CSV file `radware.csv`.

## Run as

`ansible-playbook -i inventory pb_parse_raw_data.yml `
