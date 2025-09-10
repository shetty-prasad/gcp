GCP

*******************************************************************************    IAM    *******************************************************************************    
What is IAM?
IAM controls who (identity) has what access (roles/permissions) to which resources in GCP. It allows fine-grained, policy-based access control across all Google Cloud services.

🧱 Core IAM Components
1. ✅ Identities (Who)
Identities are principals that can be granted access:

Type	Examples
Google account	user@gmail.com
Service account	service-123@project.iam.gserviceaccount.com
Google group	devs@mycompany.com
Cloud Identity domain	*@mycompany.com
Workload Identity	GKE service accounts mapped to GCP SAs
Federated Identity	External IdPs via Workload Identity Federation

2. 🧩 Resources (What)
Resources are the GCP assets you manage:

Projects

Buckets

VMs

APIs

Databases (e.g., Cloud SQL, Firestore)

IAM policies are set at:

Organization level

Folder level

Project level

Individual resource level (e.g., a specific bucket or secret)

🔄 IAM policies inherit down the hierarchy (org → folder → project → resource).

3. 🛠️ Roles (How)
A role is a collection of permissions. Types:

✅ Predefined Roles (recommended):
Maintained by Google

Example: roles/storage.objectViewer, roles/compute.instanceAdmin.v1

🛠️ Custom Roles:
Created by admins for least privilege

Useful when predefined roles are too broad

Created at project or org level

❗ Primitive Roles (avoid):
Broad access; legacy support

Owner, Editor, Viewer — too permissive for production

4. 🧾 Permissions
Permissions control actions on resources.

Example: storage.objects.get, compute.instances.start

Not assigned directly — only through roles.

5. 📄 IAM Policy Bindings
IAM policies are sets of bindings:

json
Copy
Edit
{
  "bindings": [
    {
      "role": "roles/storage.objectViewer",
      "members": [
        "user:alice@example.com",
        "serviceAccount:analytics@project.iam.gserviceaccount.com"
      ]
    }
  ]
}
6. 🔄 Policy Hierarchy
IAM policies flow top-down:

Organization – access to all GCP resources.

Folder – group related projects.

Project – typical place for most bindings.

Resource – fine-grained control (e.g., single bucket, pubsub topic).

7. 🔒 IAM Conditions (Conditional Access)
IAM Conditions allow context-aware access:

Based on resource name, request time, IP address, etc.

json
Copy
Edit
"condition": {
  "title": "Time-restricted access",
  "expression": "request.time < timestamp('2025-01-01T00:00:00Z')"
}
8. 🧠 Service Accounts
Used by applications/services to authenticate securely.

Acts as an identity and resource

Can be:

Assigned to GCE, GKE, Cloud Functions, etc.

Granted IAM roles

Used with Workload Identity or Impersonation

Workload Identity in Google Cloud Platform (GCP) IAM is a secure and manageable way for applications running outside GCP (like on-premises or in other clouds) or on GKE (Google Kubernetes Engine) to access Google Cloud services without using long-lived service account keys.

How it works:

You associate a  Kubernetes service account (KSA)  with a Google service account (GSA).
When a pod uses the KSA, GCP gives it temporary credentials to act as the GSA.

# Bind GSA to KSA
gcloud iam service-accounts add-iam-policy-binding \
  my-gcp-sa@my-project.iam.gserviceaccount.com \
  --member="serviceAccount:my-project.svc.id.goog[my-namespace/my-ksa]" \
  --role="roles/iam.workloadIdentityUser"


Workload Identity Federation
Allows external workloads (e.g., AWS, Azure, or on-premises) to federate their identity to GCP using OIDC, SAML, or AWS IAM.

How it works:

External identity (e.g., AWS role, Azure identity) is mapped to a GCP service account.
The external app exchanges its token for a GCP access token via the Workload Identity Federation API.

⚠️ Best Practice: Avoid downloading & using service account keys. Use Workload Identity or Impersonation instead.

9. 👨‍🔧 Impersonation
Allows a user/service to act on behalf of a service account.

More secure than using keys.

Useful in automation (e.g., CI/CD pipelines).

bash
Copy
Edit
gcloud auth impersonate-service-account sa-name@project.iam.gserviceaccount.com
10. 📜 Audit Logs
GCP automatically logs IAM activity via:

Admin Activity Logs: IAM policy changes

Data Access Logs: who accessed what resource

Use Cloud Logging to view logs for compliance/troubleshooting.

📊 IAM Tools & Utilities
Tool	Purpose
Policy Troubleshooter	Diagnose “why access was denied”
IAM Recommender	Suggests least privilege roles
Policy Analyzer	Check who has access to what
gcloud IAM commands	Scripting and automation
Org Policy Constraints	Enforce org-wide restrictions (e.g., disable external IPs)

🛡️ IAM Best Practices
Best Practice	Why It Matters
Use least privilege	Limit damage from misconfigurations
Prefer predefined or custom roles over primitive	More control
Use groups instead of individual users	Easier to manage
Avoid service account key files	Use Workload Identity or impersonation
Enable audit logging for sensitive resources	Compliance & troubleshooting
Periodically review IAM bindings	Prevent privilege creep
Use IAM Conditions	Context-aware access (e.g., time-bound)

🧪 Sample IAM Interview Question
Q: A contractor needs read-only access to logs for 30 days. How do you manage this?

Answer:

Add the user to a Google Group.

Assign roles/logging.viewer to the group at the project level.

Use IAM Conditions to limit access to 30 days.

Schedule a policy review/removal.

Enable audit logs to track access.

** VPC Service Controls (VPC-SC) is a Google Cloud security feature designed to mitigate data exfiltration risks by creating virtual security perimeters around your cloud resources.

Think of it as a firewall for your APIs. While IAM controls who can access a resource, VPC-SC controls where that access can come from. It helps ensure that even if credentials are compromised, data can't be accessed from outside trusted networks.

Security Command Center?
It's a centralized dashboard and service for:

Asset inventory
Vulnerability scanning
Threat detection
Compliance monitoring
Security recommendations


Private Google Access (PGA)
🎯 Purpose:
Allows VMs without external IPs to access Google APIs (e.g., BigQuery, Storage) privately, using internal IPs.

🛠️ When to Use:
VMs without public IPs
Need access to public Google APIs
Stay within Google's backbone

Private Service Access (PSA)
🎯 Purpose:
Enables VPCs to privately connect to Google-managed services in Google’s tenant projects, like:

Cloud SQL
Memorystore
AI Platform
Vertex AI

Private Service Connect (PSC)
🎯 Purpose:
Secure, private, service-to-service networking between:
Your own services (producer/consumer VPCs)
3rd-party services (e.g., MongoDB Atlas, Snowflake)

Google APIs (via PSC endpoints)

🛠️ Key Use Cases:
Expose internal load balancer to other VPCs
Connect to partner services via internal IPs
Replace Cloud NAT for API calls with PSC to Google APIs

| Feature                           | Purpose                                                               | Used For                                   | Traffic Scope                 | Example                                              |
| --------------------------------- | --------------------------------------------------------------------- | ------------------------------------------ | ----------------------------- | ---------------------------------------------------- |
| **Private Google Access (PGA)**   | Access Google APIs privately from private IP VMs                      | Google APIs (e.g. BigQuery, Cloud Storage) | VM to Google APIs             | VM in subnet with no external IP calls Cloud Storage |
| **Private Service Access (PSA)**  | Connect to **Google-managed services** over internal IP               | Cloud SQL, Memorystore, AI Platform        | VPC to Google-managed backend | VPC connects to Cloud SQL via internal IP            |
| **Private Service Connect (PSC)** | Secure private access to **partner, published, or internal services** | Your services, 3rd-party services, APIs    | VPC to VPC or VPC to Partner  | Internal load balancer exposes API to other VPCs     |



*******************************************************************************    VPC    *******************************************************************************    

What is VPC in GCP?
A VPC (Virtual Private Cloud) is a global, private, and scalable network in Google Cloud that allows your resources (VMs, Kubernetes, databases, etc.) to communicate securely with each other and the internet.

🧱 Core VPC Components
1. VPC Network
Global resource.

Contains regional subnets.

Determines routing and connectivity policies.

Can be auto mode (default subnets per region) or custom mode (you define subnets).

✅ Best Practice: Use custom mode for better control and security.

2. Subnets
Regional.

Assigned IP ranges (primary and optional secondary).

VMs and GKE nodes are deployed in subnets.

Support private Google access, flow logs, etc.

3. Routes
Define traffic flow.

Every VPC has system-generated routes (e.g., local subnet and default internet route).

Custom routes used for VPN, peering, firewalls, etc.

4. Firewall Rules
Stateful, apply at network level.

Control ingress and egress traffic to/from VMs.

Evaluated in order: allow/deny based on priority, protocol, ports, source/destination tags or IPs.

5. Peering
Connects two VPCs in the same or different projects.

Enables private RFC 1918 communication.

No transitive peering.

🔒 Routes and DNS not shared by default unless explicitly enabled.

6. Shared VPC
One host project shares VPCs with service projects.

Enables centralized network management and decentralized resource ownership.

Used in large orgs to enforce security and compliance.

7. Private Google Access
Allows VMs without public IP to reach Google APIs/services via private IPs.

Requires enabling on subnet level.

8. Cloud NAT
Network Address Translation for VMs without external IPs to access the internet.

Required for private instances to install packages, updates, etc.

9. VPC Flow Logs
Enable logging for network flows.

Useful for security monitoring, performance tuning, and auditing.

Sent to Cloud Logging.

10. Hybrid Connectivity
VPN: IPSec-based secure tunnel.

Interconnect: Dedicated/private, higher bandwidth/latency sensitive.

Partner Interconnect: Managed by GCP partners.

🛡️ VPC Best Practices
Area	Practice
Design	Use custom-mode VPC, clearly defined IP ranges
Security	Principle of least privilege on firewall rules
Routing	Avoid transitive routing issues in peering
IAM	Restrict VPC admin access using custom roles
Logging	Enable flow logs for audit and troubleshooting
Connectivity	Use Cloud NAT over public IPs for security
DNS	Use Cloud DNS and DNS peering for hybrid setups
Monitoring	Use Cloud Monitoring for route/traffic alerts

🧪 Senior GCP Admin – VPC Interview Questions & Answers
🔸 Q1: What’s the difference between Auto Mode and Custom Mode VPC?
Answer:

Auto Mode: Creates subnets automatically in all regions with predefined IP ranges.

Custom Mode: Requires manual subnet creation. Preferred for security and IP range control.

Best Practice: Always use custom mode for production networks.

🔸 Q2: How does Shared VPC work and when would you use it?
Answer:

Shared VPC allows one host project to share its network with multiple service projects.

Used to:

Centralize networking, security, and IAM

Keep application deployments decentralized

Simplify compliance

🔸 Q3: Explain VPC Peering vs VPN vs Interconnect.
Answer:

Type	Use Case	Speed	Cost
Peering	GCP-to-GCP private network	High	Low
VPN	On-prem to GCP (IPSec)	Moderate	Pay-as-you-go
Interconnect	Dedicated physical link	Very High	$$$

Use Peering for GCP internal apps.

Use VPN for basic hybrid cloud.

Use Interconnect for enterprise-grade latency-sensitive apps.

🔸 Q4: How do you isolate environments (dev/test/prod) in a VPC design?
Answer:

Create separate subnets per environment or separate projects with Shared VPC.

Use firewall rules and service accounts to enforce boundaries.

Leverage network tags and IAM to separate access.

Use VPC Service Controls for data exfiltration prevention between environments.

🔸 Q5: What is Cloud NAT and why is it important?
Answer:

Cloud NAT allows VMs without public IPs to access the internet securely.

Key for:

Security (no external IP exposure)

Installing software/updates on private VMs

Saving public IP costs

🔸 Q6: What happens if two peered VPCs have overlapping IP ranges?
Answer:

Peering will fail.

GCP does not allow overlapping CIDR blocks between peered VPCs.

You must plan IP ranges carefully using IPAM tools or spreadsheets.

🔸 Q7: How do you troubleshoot a VM unable to access the internet?
Checklist:

Does it have an external IP?

Is Cloud NAT configured for the subnet?

Firewall rules allowing egress?

Routing table includes default internet route?

VPC flow logs for dropped packets?

🔸 Q8: How do you monitor and secure network traffic in a VPC?
Answer:

Use VPC Flow Logs + Cloud Logging.

Set up alerts in Cloud Monitoring for unusual spikes.

Use firewall logging to detect blocked or suspicious access.

Enable SCC (Security Command Center) and Threat Detection.

Use Cloud IDS for advanced traffic inspection (if needed).

🔸 Q9: What are secondary IP ranges in subnets used for?
Answer:

Used by GKE for Pod IPs and Service IPs.

Required when using alias IPs.

Allows isolation of workload traffic from control plane or system traffic.

🔸 Q10: How does Private Google Access work?
Answer:

Allows VMs without public IPs to access Google APIs/services.

Enabled at the subnet level.

Required for:

GKE nodes without external IPs

Private App Engine/GCS/BigQuery access


*******************************************************************************    Cloud Storage    *******************************************************************************    

What is Cloud Storage?
Cloud Storage is Google’s object storage service for any amount of data. It's highly durable, globally available, and designed for unstructured data like backups, logs, videos, archives, and data lakes.

It stores objects (files) in buckets, with built-in capabilities like versioning, lifecycle management, and encryption.

🧱 Key Components
Component	Description
Buckets	Logical containers for storing data objects. Each bucket has a globally unique name and is created in a specific location (region, dual-region, multi-region).
Objects	The actual data stored — e.g., files, images, videos. Each object includes data and metadata.
Classes	Storage tiers for cost vs access trade-off (Standard, Nearline, Coldline, Archive).
Access Control	IAM, ACLs, and Signed URLs to manage access to buckets/objects.
Encryption	Supports Google-managed keys, customer-managed keys (CMEK), and customer-supplied keys (CSEK).

🗂️ Storage Classes
Class	Use Case	Min Storage Duration	Retrieval Cost	Examples
Standard	Frequently accessed data	None	Low	Websites, daily analytics
Nearline	Access ~once/month	30 days	Medium	Monthly logs, backups
Coldline	Access ~once/quarter	90 days	Higher	Quarterly backups
Archive	Rare access (long-term archive)	365 days	Highest	Legal archives, compliance

📍 Locations
Regional – for lower latency, compute proximity

Dual-Region – automatic replication across 2 regions (e.g., ASIA1)

Multi-Region – higher availability (e.g., US, EU)

🔐 Access Management Options
IAM Roles – Bucket- or project-level access (e.g., roles/storage.objectViewer)

ACLs – Fine-grained legacy control (less recommended)

Signed URLs – Temporary, tokenized URL for time-limited access

Signed Policy Documents – For browser-based uploads

⚙️ Lifecycle Rules
Automatically manage object aging, e.g.:

json
Copy
Edit
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 365}
    }
  ]
}
🧪 Examples
🔹 Create a bucket:
bash
Copy
Edit
gsutil mb -l us-central1 gs://my-company-data-bucket/
🔹 Upload a file:
bash
Copy
Edit
gsutil cp ./sales.csv gs://my-company-data-bucket/
🔹 Set IAM permissions:
bash
Copy
Edit
gsutil iam ch user:alice@example.com:objectViewer gs://my-company-data-bucket/
🔹 Enable versioning:
bash
Copy
Edit
gsutil versioning set on gs://my-company-data-bucket/
🔹 List all versions:
bash
Copy
Edit
gsutil ls -a gs://my-company-data-bucket/myfile.txt
🛡️ Cloud Storage Best Practices
Enable Object Versioning for rollback.

Use lifecycle rules to auto-delete old data.

Use customer-managed encryption (CMEK) for sensitive data.

Use VPC-SC to protect against data exfiltration.

Avoid public buckets unless required and audit them regularly.

Use Signed URLs instead of permanent access for temporary sharing.

Turn on Audit Logs to track data access.

👨‍💼 Senior GCP Admin Interview Questions on Cloud Storage
🔸 Q1: How do you secure a bucket to ensure only specific users can access it?
Answer:

Use IAM roles at bucket level:

bash
Copy
Edit
gsutil iam ch user:bob@example.com:objectViewer gs://secure-bucket/
Disable Uniform Bucket-Level Access if fine-grained control needed.

Turn on audit logs and monitor Cloud SCC for open access.

🔸 Q2: Explain the use of Signed URLs and when to use them.
Answer:

Signed URLs are temporary access URLs to specific objects.

Useful for:

Giving time-bound access to external users without IAM setup.

Integrating with web apps for private downloads.

Example:

bash
Copy
Edit
gsutil signurl -d 10m private-key.json gs://my-bucket/private-file.txt
🔸 Q3: How do you handle data lifecycle and archiving in GCS?
Answer:

Use storage classes based on access frequency.

Create lifecycle management rules to transition or delete old data.

Example: Move to Archive after 1 year, delete after 5 years.

Helps optimize cost without losing compliance.

🔸 Q4: What is Uniform Bucket-Level Access (UBLA)?
Answer:

UBLA disables object-level ACLs, simplifying permission management.

Enforces IAM-only access.

Recommended for production buckets to avoid misconfigurations.

🔸 Q5: What’s the difference between Nearline, Coldline, and Archive?
Class	Min Duration	Use Case	Retrieval Cost
Nearline	30 days	Infrequent monthly access	Low
Coldline	90 days	Quarterly access	Higher
Archive	365 days	Long-term storage	Highest

🔸 Q6: How would you integrate GCS with on-prem systems?
Answer:

Use gsutil or Storage Transfer Service for scheduled sync.

Optionally set up Transfer Appliance for petabyte-scale imports.

Use VPN/Interconnect + Private Google Access for secure upload.

🔸 Q7: How do you prevent public data exposure in Cloud Storage?
Answer:

Use Cloud Security Command Center to scan for open buckets.

Enforce Org Policies:

constraints/storage.publicAccessPrevention = enforced

Enable UBLA and avoid using legacy ACLs.

Audit with Cloud Audit Logs.

🔸 Q8: How does CMEK work in GCS?
Answer:

You create a key in Cloud KMS.

Assign it to the bucket:

bash
Copy
Edit
gsutil kms set-key \
projects/your-project/locations/global/keyRings/kr/cryptoKeys/key \
gs://your-bucket
Only users with access to KMS key can read/write data.

Useful for compliance (HIPAA, GDPR, etc.).

🔸 Q9: How do you automate GCS bucket provisioning securely?
Answer:

Use Terraform or Deployment Manager.

Define lifecycle rules, IAM policies, encryption, logging in code.

Example Terraform:

hcl
Copy
Edit
resource "google_storage_bucket" "logs" {
  name     = "my-log-bucket"
  location = "US"
  force_destroy = true

  lifecycle_rule {
    action { type = "Delete" }
    condition { age = 365 }
  }

  uniform_bucket_level_access = true
}
🔸 Q10: How do you monitor and audit access to Cloud Storage?
Answer:

Enable Cloud Audit Logs:

Admin Activity and Data Access

Use log-based metrics to alert on unusual access.

Optionally integrate with SIEM tools.

Enable Bucket Logging to another log bucket.

*******************************************************************************    Compute instance    *******************************************************************************    

What is Compute Engine?
Google Compute Engine (GCE) is GCP’s Infrastructure-as-a-Service (IaaS) that allows users to create and run virtual machines (VMs) on Google’s infrastructure. You can customize machine types, attach GPUs, manage disks, set startup scripts, and more.

🧱 Key Components of Compute Engine
1. Instance (VM)
A virtual machine running on GCP.

Can be Linux or Windows, with full SSH or RDP access.

Launched using a boot disk (persistent disk or custom image).

2. Machine Types
Predefined (e2, n2, n2d, c2, a2, t2a, etc.)

Custom (vCPU and RAM as per need)

Specialized (with GPUs, TPUs)

Machine Family	Use Case
e2	Cost-efficient general purpose
n2/n2d	Balanced compute and memory
c2/c3	Compute-intensive workloads
a2	ML workloads (GPU-heavy)
t2a	ARM-based workloads

3. Persistent Disks
Attached to VMs; survive instance termination.

Types: Standard, Balanced, SSD, Extreme.

Support snapshots, resize, and multi-attach.

4. Instance Templates & Groups
Templates define a VM configuration for reuse.

Managed instance groups (MIGs) support:

Auto-scaling

Auto-healing

Rolling updates

5. Startup & Shutdown Scripts
Automate installation, logging, or tasks at boot time.

bash
Copy
Edit
#! /bin/bash
sudo apt update
sudo apt install -y nginx
6. Service Accounts
VMs use service accounts to authenticate to GCP services.

Apply minimum IAM permissions (least privilege).

7. Preemptible / Spot Instances
Short-lived, highly discounted VMs.

Good for batch jobs, stateless workloads.

8. Shielded VMs
Protect against bootkits and rootkits.

Use Secure Boot, vTPM, and Integrity Monitoring.

9. Live Migration
GCP supports live migration of VMs during host maintenance with no downtime.

10. Labels & Tags
Useful for cost allocation, automation, firewall rules, and inventory tracking.

🔧 Examples
🔹 Create a basic VM:
bash
Copy
Edit
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud
🔹 Add a startup script:
bash
Copy
Edit
gcloud compute instances create web-server \
  --metadata=startup-script='#! /bin/bash
    apt-get update
    apt-get install -y apache2
    systemctl start apache2'
🔹 Create a VM with a custom image:
bash
Copy
Edit
gcloud compute instances create custom-vm \
  --image=my-custom-image \
  --image-project=my-project
🔹 Attach a persistent disk:
bash
Copy
Edit
gcloud compute instances attach-disk my-vm \
  --disk=my-disk --zone=us-central1-a
🛡️ Best Practices
Area	Best Practice
Security	Use service accounts with least privilege, disable root SSH
Networking	Use VPC firewall rules and internal IPs
Storage	Use snapshots and disk resizing proactively
Monitoring	Use Cloud Monitoring, enable logging and uptime checks
Automation	Use Instance Templates, Terraform, or Deployment Manager
Scaling	Use MIGs for autoscaling and high availability
Cost	Use Committed Use Discounts or Spot instances when possible
Backup	Automate snapshot schedules using policies

🎯 Interview Questions & Answers – Senior GCP Admin Role
🔸 Q1: What happens during a live migration of a VM?
Answer:

GCP automatically migrates VMs without downtime during maintenance events.

RAM and local SSD content are preserved.

VMs remain accessible to users.

🔸 Q2: How do you secure a Compute Engine VM?
Answer:

Use Shielded VM features (Secure Boot, vTPM).

Apply OS Login for SSH access control.

Disable project-wide SSH keys.

Use firewall rules to restrict ports (allow only 22/80/443).

Use CMEK to encrypt disks.

Attach VMs to private subnets when possible.

🔸 Q3: How do you auto-scale your application using Compute Engine?
Answer:

Use Managed Instance Groups (MIGs):

Create Instance Template.

Define scaling policy (CPU utilization, load balancing).

GCP automatically adds/removes instances based on traffic/load.

🔸 Q4: What are the differences between a snapshot and an image?
Feature	Snapshot	Image
Scope	Disk-level	Bootable disk with OS
Use	Backup and restore	Create new VMs
Incremental?	Yes	No
Customizable?	Snapshot of any disk	Typically boot disks

🔸 Q5: How do you automate VM provisioning?
Answer:

Use:

Instance Templates for standard configs.

Terraform or Deployment Manager for infrastructure-as-code.

Startup scripts to install/configure software.

🔸 Q6: How do preemptible (spot) VMs work?
Answer:

Short-lived (max 24 hrs), cheap VMs.

Can be terminated anytime with a 30s warning.

Use for stateless, batch, or fault-tolerant workloads.

Up to 91% cheaper than standard VMs.

🔸 Q7: What is the difference between internal and external IPs?
IP Type	Use
Internal IP	Private communication within the VPC
External IP	Publicly accessible; used for internet-facing apps

Use NAT Gateway (Cloud NAT) to give internal VMs outbound internet access without public IPs.

🔸 Q8: How do you monitor performance and availability of VMs?
Answer:

Use Cloud Monitoring:

Metrics: CPU, memory, disk, network

Uptime Checks

Use Cloud Logging for logs

Enable agent-based monitoring for deeper OS metrics

🔸 Q9: What happens when a VM is stopped vs terminated?
State	Explanation
Stopped	Billing for compute stops, but disk costs continue
Terminated	VM is deleted; data on ephemeral disks lost, persistent disks survive

🔸 Q10: What is a MIG (Managed Instance Group) and how is it different from an Unmanaged Group?
Feature	Managed IG	Unmanaged IG
Auto-scaling	✅	❌
Auto-healing	✅	❌
Load Balancing	✅	✅
Use Case	Stateless, scalable apps	Legacy/manual VMs

✅ Final Tips for Interviews
Be ready to explain real-world VM architectures (e.g., HA web tier with MIGs + Load Balancer).

Know the cost optimization strategies using custom/spot VMs.

Be clear on security layers: IAM, SSH keys, firewall rules, service accounts.

Understand how to migrate workloads using Migrate for Compute Engine or image import.

Mention Terraform or automation if asked about scaling or repeatable deployments.


