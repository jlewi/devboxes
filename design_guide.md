# Devbox Design Guide

## Tailscale 

We use [tailscale-ssh](https://tailscale.com/kb/1193/tailscale-ssh?slug=kb&slug=1193&slug=tailscale-ssh)
to run an ssh server accessible over VPN
* Using tailscale ssh means we control who can access the ssh servers using tailscale ACLS

### Tailscale ACLs

Here's an example ACL that would allow anyone to ssh into a devbox.
We should probably make these user specific.
to ssh into any machine tagged *devbox*

```
// Added by jeremy to support devboxes
// Allow any user to ssh to any machine
{
    "action": "accept",
    "src":    ["autogroup:member"],
    "dst":    ["tag:devbox"],
    "users":  ["autogroup:nonroot", "root"],
},
```

### Authorizing Devboxes - Auth Keys 

We use [auth-keys](https://tailscale.com/kb/1068/acl-tags#generate-an-auth-key-with-an-acl-tag)
to Authorize devboxes to connect to the tailscale.

* The AuthKey can be stored in a GCP secret 
* We use an AuthKey with following properties
  * Reusable
  * Ephmeral
  * Tags - "devbox"
    * This way devices created with the key automatically get tagged


  