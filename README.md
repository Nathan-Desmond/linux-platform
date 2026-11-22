# Linux Platform Homelab

A self-built platform engineering lab that provisions, configures, deploys and monitors Linux servers using infrastructure as code.

## Lab environment
- Host: Windows 11 + WSL2 (Ubuntu)
- Servers: 2x Ubuntu 24.04 LXD system containers simulating a multi-server environment
  - `web1` - application server
  - `mon1` - monitoring server

## Stack
| Area | Tool | Status |
|---|---|---|
| Servers | LXD | Done |
| Configuration management | Ansible | In Progress |
| Containers | Docker | Not Started |
| CI/CD | GitHub Actions | Not Started |
| Monitoring | Prometheus + Grafana | Not Started |
| Infrastructure as code | Terraform | Not started |

## Progress
- [x] Stage 1: Lab servers, SSH key auth, Ansible connectivity
- [ ] Stage 2: Server hardening with Ansible
