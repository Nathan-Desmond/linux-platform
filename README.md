# Linux Platform Homelab

A self-built platform engineering lab that provisions, configures, deploys and monitors Linux servers using infrastructure as code.

## Lab environment
- Host: Windows 11 + WSL2 (Ubuntu)
- Servers: 2x Ubuntu 24.04 LXD system containers simulating a multi-server environment
  - `web1` (10.220.245.17) - application server
  - `mon1` (10.220.245.83) - monitoring server
- Access: SSH key authentication only, fixed IPs

## Stack
| Area | Tool | Status |
|---|---|---|
| Servers | LXD | Done |
| Configuration management | Ansible | Done |
| Containers | Docker | Planned |
| CI/CD | GitHub Actions | Planned |
| Monitoring | Prometheus + Grafana | Planned |
| Infrastructure as code | Terraform | Planned |

## Server hardening (Ansible role: `common`)
Applied to every server with `ansible-playbook site.yml`:
- Creates a `devops` admin user with SSH key login and sudo access
- SSH: root login disabled, password login disabled, max 3 auth attempts
- Firewall (ufw): deny all incoming except SSH, allow outgoing
- Automatic security updates enabled (unattended-upgrades)
- Config files validated before being written (`visudo`, `sshd -t`) to prevent lockouts
- Idempotent: a second run reports `changed=0`

## Usage
```bash
cd ansible
ansible all -m ping              # check connectivity
ansible-playbook site.yml        # apply configuration
cat > README.md <<'EOF'
# Linux Platform Homelab

A self-built platform engineering lab that provisions, configures, deploys and monitors Linux servers using infrastructure as code.

## Lab environment
- Host: Windows 11 + WSL2 (Ubuntu)
- Servers: 2x Ubuntu 24.04 LXD system containers simulating a multi-server environment
  - `web1` (10.220.245.17) - application server
  - `mon1` (10.220.245.83) - monitoring server
- Access: SSH key authentication only, fixed IPs

## Stack
| Area | Tool | Status |
|---|---|---|
| Servers | LXD | Done |
| Configuration management | Ansible | Done |
| Containers | Docker | Planned |
| CI/CD | GitHub Actions | Planned |
| Monitoring | Prometheus + Grafana | Planned |
| Infrastructure as code | Terraform | Planned |

## Server hardening (Ansible role: `common`)
Applied to every server with `ansible-playbook site.yml`:
- Creates a `devops` admin user with SSH key login and sudo access
- SSH: root login disabled, password login disabled, max 3 auth attempts
- Firewall (ufw): deny all incoming except SSH, allow outgoing
- Automatic security updates enabled (unattended-upgrades)
- Config files validated before being written (`visudo`, `sshd -t`) to prevent lockouts
- Idempotent: a second run reports `changed=0`

## Usage
~~~bash
cd ansible
ansible all -m ping              # check connectivity
ansible-playbook site.yml        # apply configuration
~~~

## Progress
- [x] Stage 1: Lab servers, SSH key auth, Ansible connectivity
- [x] Stage 2: Server hardening with Ansible
- [ ] Stage 3: Containerised app deployed with Ansible + Docker
- [ ] Stage 4: CI/CD with GitHub Actions
- [ ] Stage 5: Monitoring with Prometheus + Grafana
- [ ] Stage 6: Terraform
- [ ] Stage 7: Kubernetes (k3d)
- [ ] Stage 8: Deploy to a cloud VM
