This is demonstration project where Raspberry PI sends temperature and humidity
data read from connected sensor to InfluxDB database running in Azure cloud.
The data can be viewed using Grafana GUI.

InfluxDB and Grafana are installed in Docker containers in CentOS based VMs
and pre-configured with the required database and dashboards.

Information about the used sensor:
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated

Python script to be executed as cron task in Raspberry is in scripts directory.
The installation of script and drivers on Raspberry side is not included
in Ansible automation.


Preconditions:

In CentOS or Fedora client, install pip:
sudo yum install epel-release -y
sudo yum install python-pip -y

Install Ansible:
sudo pip install ansible

Install python module "azure":
sudo pip install ansible[azure]

Update version of msrestazure package as otherwise you may face certificate verification failure:
sudo pip install msrestazure -U

Make sure that your private key is loaded in SSH-agent and agent forwarding is enabled in your SSH session.

Setup steps:
- Clone git repo with "git clone https://github.com/jurajama/TempMonitor"
cd TempMonitor

- Modify personal_config.yml in group_vars/all with your own settings:
    - az_ssh_public_key shall be your public SSH key
    - az_admin_username is the bootstrap user created in VM. It needs to be the same as the user in the host where you run Ansible, or if not then you shall modify hosts file so that you define ansible_user=yourusername for dbservers.

- Update external roles:
./update_roles.bash

Source azure credentials, that is environment variables:
export AZURE_SUBSCRIPTION_ID=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
export AZURE_CLIENT_ID=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
export AZURE_SECRET=xxxxxxxx
export AZURE_TENANT=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

- Run playbook
ansible-playbook config-dbserver.yml

After successful execution you can find the public IP of the created VM from Ansible console outputs
or from Azure GUI.


Uninstallation:
Remove all resources by deleting the Resource Group via Azure GUI.

