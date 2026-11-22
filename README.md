# Linux Platform Homelab

A self-built platform engineering lab that provisions, configures, deploys and monitors Linux servers using infrastructure as code.

## Architecture
~~~text
 Laptop (Windows 11 + WSL2 Ubuntu)
 |
 |-- Ansible (control node) -- SSH keys --+
 |                                        |
 |   LXD bridge network 10.220.245.0/24   |
 |                                        v
 |   +-------------------------+   +-------------------------+
 |   | web1  10.220.245.17     |   | mon1  10.220.245.83     |
 |   | Ubuntu 24.04 (LXD)      |   | Ubuntu 24.04 (LXD)      |
 |   | ufw, hardened SSH       |   | ufw, hardened SSH       |
 |   | Docker                  |   | Docker                  |
 |   |  +-------------------+  |   |  (monitoring - Stage 5) |
 |   |  | homelab-app       |  |   |                         |
 |   |  | gunicorn + Flask  |  |   |                         |
 |   |  | :80 -> :5000      |  |   |                         |
 |   |  +-------------------+  |   |                         |
 |   +-------------------------+   +-------------------------+
~~~

## Lab environment
- Host: Windows 11 + WSL2 (Ubuntu), 8 GB RAM, WSL capped at 4 GB
- Servers: 2x Ubuntu 24.04 LXD system containers with fixed IPs, memory limits and nesting enabled for Docker
- Access: SSH key authentication only

## Stack
| Area | Tool | Status |
|---|---|---|
| Servers | LXD | Done |
| Configuration management | Ansible | Done |
| Containers | Docker | Done |
| CI/CD | GitHub Actions | Planned |
| Monitoring | Prometheus + Grafana | Planned |
| Infrastructure as code | Terraform | Planned |

## Repository layout
~~~text
ansible/
  ansible.cfg            project defaults
  inventory.ini          servers and groups
  site.yml               play 1: common + docker on all servers
                         play 2: app on web servers
  roles/
    common/              hardening: admin user, SSH, firewall, auto-updates
    docker/              Docker Engine from Docker's signed apt repo
    app/                 build image on server, run container, smoke test
app/
  app.py                 Flask app with / and /health endpoints
  requirements.txt       pinned dependencies
  Dockerfile             slim base, non-root user, healthcheck, layer caching
~~~

## Roles
**common** (all servers)
- `devops` admin user with SSH key and sudo
- SSH: root login and password login disabled, max 3 auth attempts
- ufw: deny incoming except SSH, allow outgoing
- Automatic security updates
- Config validated before writing (`visudo`, `sshd -t`) to prevent lockouts

**docker** (all servers)
- Installs Docker Engine, Buildx and Compose from Docker's signed repository
- Adds admin user to the `docker` group

**app** (web servers)
- Copies app source, rebuilds the image only when code changes
- Runs the container with a restart policy and version passed as an environment variable
- Smoke test: deploy fails unless `/health` returns 200

## Usage
~~~bash
cd ansible
ansible all -m ping                             # check connectivity
ansible-playbook site.yml                       # configure servers and deploy app
ansible-playbook site.yml -e app_version=1.1.0  # deploy a specific version
curl http://10.220.245.17                       # call the app
~~~

## Verified behaviour
- Idempotent: second run reports `changed=0`
- Version deploy and rollback using tagged images
- App restarts automatically after a server reboot
- Configuration drift (deleted container, removed firewall rule) repaired by re-running the playbook

## Lessons learned
- Docker-published ports bypass ufw because Docker inserts iptables rules ahead of ufw's. A host firewall alone does not protect containers; use bind addresses, the `DOCKER-USER` chain or an external (cloud) firewall.
- SSH reads the first value it finds, so the hardening file is named `00-hardening.conf` to take priority over distro defaults.
- Running Docker inside LXD requires `security.nesting` and syscall interception settings.

## Progress
- [x] Stage 1: Lab servers, SSH key auth, Ansible connectivity
- [x] Stage 2: Server hardening with Ansible
- [x] Stage 3: Containerised app deployed with Ansible + Docker
- [ ] Stage 4: CI/CD with GitHub Actions
- [ ] Stage 5: Monitoring with Prometheus + Grafana
- [ ] Stage 6: Terraform
- [ ] Stage 7: Kubernetes (k3d)
- [ ] Stage 8: Deploy to a cloud VM
