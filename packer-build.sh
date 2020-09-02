# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#  This shell file is compiled from Google Cloud Solutions "Using Jenkins for distributed builds on Compute Engine".
#  You can follow the tutorial here: (https://cloud.google.com/solutions/using-jenkins-for-distributed-builds-on-compute-engine)

ls ~/.ssh/id_rsa.pub || ssh-keygen -N ""

gcloud compute project-info describe \
    --format=json | jq -r '.commonInstanceMetadata.items[] | select(.key == "ssh-keys") | .value' > sshKeys.pub
echo "$USER:$(cat ~/.ssh/id_rsa.pub)" >> sshKeys.pub
gcloud compute project-info add-metadata --metadata-from-file ssh-keys=sshKeys.pub

wget https://releases.hashicorp.com/packer/0.12.3/packer_0.12.3_linux_amd64.zip
echo "y" | unzip packer_0.12.3_linux_amd64.zip
export PROJECT=$(gcloud info --format='value(config.project)')
cat > jenkins-agent.json <<EOF
{
  "builders": [
    {
      "type": "googlecompute",
      "project_id": "$PROJECT",
      "source_image_family": "ubuntu-2004-lts",
      "source_image_project_id": "ubuntu-os-cloud",
      "zone": "asia-east1-a",
      "disk_size": "10",
      "image_name": "jenkins-agent-{{timestamp}}",
      "image_family": "jenkins-agent",
      "ssh_username": "ubuntu"
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": ["sudo apt-get update",
                  "sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common",
                  "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
                  "sudo apt-key fingerprint 0EBFCD88",
                  "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
                  "sudo apt-get update",
                  "sudo apt-get install -y docker-ce docker-ce-cli containerd.io",
                  "sudo apt-get install -y default-jdk",
                  "sudo apt-get update && sudo apt-get install -y google-cloud-sdk"]
    }
  ]
}
EOF

./packer build jenkins-agent.json