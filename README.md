# o11y-ansible-demo
NOTE: These instructions assume an Ubuntu 22.04 instance with python3 already installed. I used a t2.medium; you may be able to use a smaller instance.

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
sudo apt install -y ansible
sudo mkdir /etc/ansible
sudo cp ~/o11y-ansible-demo/ansible-hosts /etc/ansible/hosts
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
* Add kubernetes plugin
```
ansible-galaxy collection install kubernetes.core
```
## Install k3s and Docker
* Install k3s
```
curl -sfL https://get.k3s.io | sh -
sudo chmod 755 /etc/rancher/k3s/k3s.yaml
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```
* Install docker
```
sudo apt-get install -y ca-certificates curl gnupg lsb-release
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
* Install python3, pip, and dependencies
```
sudo apt install -y python3 python3-pip
```
* Setup the ansible-manager environment
```
cd ~/o11y-ansible-demo/ansible-manager
sudo pip3 install -r requirements.txt
```
* Build the apps
```
cd ~/o11y-ansible-demo/app_v1
docker build -t sampleapp:1 .

cd ~/o11y-ansible-demo/app_v2
docker build -t sampleapp:2 .
```
* Add the apps to k3s
```
cd ~

docker save --output sampleapp-v1.tar sampleapp:1
sudo k3s ctr images import sampleapp-v1.tar

docker save --output sampleapp-v2.tar sampleapp:2
sudo k3s ctr images import sampleapp-v2.tar
```

* Deploy v1 of the app
```
cd ~/o11y-ansible-demo
kubectl apply -f v1.yml
```

## Start the ansible manager
```
cd ~/o11y-ansible-demo/ansible-manager
sudo flask run --host=0.0.0.0 --port=81
```