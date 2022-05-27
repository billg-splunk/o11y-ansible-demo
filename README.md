# o11y-ansible-demo
NOTE: These instructions assume an Ubuntu 22.04 instance with python3 already installed.

It does not setup a venv, but this is generally a best practice.

You may need to make minor modifications to install some dependencies.
## Download this repo
```
cd ~
git clone https://github.com/billg-splunk/o11y-ansible-demo.git
```

## Setup Ansible
* Install Ansible
```
sudo apt update
sudo apt install ansible
mkdir /etc/ansible
cp ~/o11y-ansible-demo/ansible-hosts /etc/ansible/hosts
```
* Test the ping
```
ansible all -m ping
```
* You should get a successful ping
```
127.0.0.1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

## Install k3s and Docker
* Install k3s
```
curl -sfL https://get.k3s.io | sh -
sudo chmod 755 /etc/rancher/k3s/k3s.yaml
```
* Install docker
```
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```
## Install the Apps
We will run the ansible manager directly on the system and we will run the web app using k3s. An Ansible playbook will toggle the version of the app.
* Setup the ansible-manager environment
```
cd ~/o11y-ansible-demo/ansible-manager
pip install -r requirements.txt
```
* Build the apps
```
cd ~/o11y-ansible-demo/app_v1
docker build -t sampleapp:1 .
cd ~/o11y-ansible-demo/app_v2
docker build -t sampleapp:2 .
```
* Deploy v1 of the app
```
cd ~/o11y-ansible-demo
kubectl apply -f v1.yml
```