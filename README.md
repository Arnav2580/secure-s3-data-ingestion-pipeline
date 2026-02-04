# Secure S3 Data Ingestion Pipeline (Serverless)

A **secure, serverless data ingestion pipeline** built on AWS using **Amazon S3, AWS Lambda, DynamoDB, IAM, KMS, CloudTrail, and CloudWatch**.  
The project focuses on **cloud security best practices**, **least-privilege IAM**, **encryption in transit and at rest**, and **full auditability**, aligned with **CIS Critical Security Controls v8**.

This repository is self-contained: a new user can understand the architecture, security decisions, and implement the project in their own AWS account by following this README.

---

## 📌 Problem Statement

Traditional data ingestion pipelines often suffer from:
- Over-privileged access (admin roles, shared credentials)
- Unencrypted data at rest or in transit
- Lack of audit trails for security and compliance
- Manual scripts and delayed data availability

This project addresses these issues by building a **serverless, event-driven ingestion pipeline** where:
- Data is uploaded securely to S3
- Processing happens automatically using AWS Lambda
- Structured records are stored in DynamoDB
- All access is controlled using IAM roles
- All actions are logged and auditable

---

## 🏗️ Architecture Overview

### High-level Flow (Mermaid Diagram)

```mermaid
flowchart TD
    A[Client uploads JSON file] -->|HTTPS only| B[S3 Bucket<br/>SSE-KMS enabled]
    B -->|ObjectCreated event| C[AWS Lambda<br/>IAM execution role]
    C -->|PutItem / BatchWriteItem| D[DynamoDB<br/>Encrypted at rest]
    B --> E[CloudTrail]
    C --> E
    D --> E
    C --> F[CloudWatch Logs]
````

### Architecture Explanation

1. A producer uploads a raw JSON file to an S3 bucket.
2. The S3 bucket enforces HTTPS-only access and encrypts objects using AWS KMS.
3. An `ObjectCreated` event triggers a Lambda function.
4. Lambda reads the file, validates records, and writes structured data to DynamoDB.
5. All API actions are recorded by CloudTrail.
6. Lambda execution details are logged in CloudWatch.

There are **no servers**, **no open ports**, and **no long-lived credentials**.

---

## 🔐 Security Design Principles

* **Least privilege**: Each service has only the permissions it needs.
* **No IAM users for services**: Only IAM roles are used.
* **Encryption everywhere**:

  * HTTPS for data in transit
  * SSE-KMS for data at rest
* **Explicit deny policies** for enforcing security constraints.
* **Defense in depth** using IAM policies + KMS key policies.
* **Auditability by default** using CloudTrail and CloudWatch.

---

## 🔑 AWS Services Used

| Service    | Purpose                        |
| ---------- | ------------------------------ |
| Amazon S3  | Entry point for raw JSON data  |
| AWS Lambda | Serverless data processing     |
| DynamoDB   | Structured data storage        |
| IAM        | Identity and access management |
| AWS KMS    | Encryption key management      |
| CloudTrail | Audit logging                  |
| CloudWatch | Logs and metrics               |

---

## 📁 Repository Structure

```
secure-s3-data-ingestion-pipeline/
│
├── README.md
├── lambda/
│   └── ingestion_lambda.py
│
├── iam/
│   ├── trust_policy.json
│   └── lambda_execution_role_policy.json
│
├── s3/
│   └── bucket_policy_https_only.json
│
├── kms/
│   └── kms_key_policy.json
│
├── docs/
│   └── security-implementation.md
│
└── screenshots/
```

Each folder maps directly to an AWS security component used in the project.

---

## 🔐 IAM Design (Important)

### Root Account

* Exists only for account ownership and billing.
* **Not used** for any operational tasks.

### IAM Roles

* A single **Lambda execution role** is used.
* The role:

  * Can read objects from the specific S3 bucket.
  * Can write records to the specific DynamoDB table.
  * Can decrypt data using a specific KMS key.
  * Can write logs to CloudWatch.

There are:

* No IAM users
* No access keys
* No secrets in code

---

## 🔒 Encryption Model

### Data in Transit

* S3 bucket policy denies any request that is not using HTTPS.

### Data at Rest

* S3 objects are encrypted using **SSE-KMS**.
* DynamoDB table uses encryption at rest.
* KMS key rotation is enabled.

Lambda never accesses encryption keys directly.

---

## 📜 Logging and Auditability

### CloudTrail

* Enabled as a **multi-region trail**.
* Logs:

  * S3 object-level events
  * IAM changes
  * Lambda and DynamoDB API calls
* Log file validation is enabled to detect tampering.

### CloudWatch

* Lambda execution logs
* Error and invocation metrics
* Used for debugging and operational visibility

---

## 🚀 Step-by-Step AWS Implementation Guide

### Step 1: Create S3 Bucket

1. Go to **Amazon S3 → Create bucket**
2. Choose a unique bucket name
3. Block all public access
4. Enable bucket versioning
5. Enable default encryption using **AWS KMS**

---

### Step 2: Create KMS Key

1. Go to **AWS KMS → Create key**
2. Create a symmetric customer-managed key
3. Enable automatic key rotation
4. Allow S3 and Lambda to use the key

---

### Step 3: Apply S3 Bucket Policy

* Apply the policy from `s3/bucket_policy_https_only.json`
* This enforces HTTPS-only access

---

### Step 4: Create DynamoDB Table

1. Table name: `ProcessedRecords`
2. Partition key: `device_id` (String)
3. Sort key: `timestamp` (String)
4. Use on-demand capacity

---

### Step 5: Create IAM Role for Lambda

1. Go to **IAM → Roles → Create role**
2. Trusted entity: AWS Lambda
3. Attach policy from `iam/lambda_execution_role_policy.json`

---

### Step 6: Create Lambda Function

1. Go to **AWS Lambda → Create function**
2. Runtime: Python 3.x
3. Attach the IAM role created above
4. Set environment variable:

   * `TABLE_NAME=ProcessedRecords`
5. Paste code from `lambda/ingestion_lambda.py`

---

### Step 7: Configure S3 Event Trigger

1. Open the S3 bucket
2. Add an event notification for `ObjectCreated`
3. Set Lambda function as destination

---

### Step 8: Enable CloudTrail

1. Create a multi-region trail
2. Enable management and S3 data events
3. Enable log file validation

---

### Step 9: Monitor with CloudWatch

* Verify Lambda logs
* Check error and invocation metrics

---

## 🧪 How to Test

Upload a JSON file to S3:

```json
[
  {
    "device_id": "device-001",
    "timestamp": "2026-02-01T10:00:00Z",
    "value": 42
  }
]
```

Verify:

* Lambda is triggered
* Record appears in DynamoDB
* Events appear in CloudTrail
* Logs appear in CloudWatch

---

## 📊 CIS Controls Alignment

* **CIS 3** – Data Protection
* **CIS 5** – Account Management
* **CIS 6** – Access Control Management
* **CIS 8** – Audit Log Management
* **CIS 11** – Data Recovery

---

## ⚠️ Security Notes

* All configuration files are sanitized.
* No secrets, access keys, or account IDs are stored.
* Intended for academic and learning purposes.

---

## ✅ Key Takeaway

This project demonstrates how a **secure cloud ingestion pipeline** can be built using AWS managed services, IAM roles, encryption, and audit logging—without servers or long-lived credentials.

---
