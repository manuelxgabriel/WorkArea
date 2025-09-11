# AWS CDK (Python) - VPC Creation Guide

This guide walks you through creating an **Amazon VPC with 
six public subnets*** using the ***AWS Cloud Development Kit
(CDK)** in Python. You'll learn how to:

- Set up a CDK project
- Define a VPC with 6 public subnets
- Deploy your infrastructure with a CDK CLI

___

## 🔧 Prerequisites
1. **Install Node.js** (required for CDK CLI)
    ```bash
   # MacOS
   brew install node
   
   # Ubuntu/Debian
   sudo apt update && apt install nodejs npm -y
   ```
2. **Install CDK CLI**
    ```bash
    npm install -g aws-cdk
    ```
3. **Install python & virtualenv**
    ```bash
        python3 -m venv .venv
        source .venv/bin/activate
    ```
4. **Install AWS CDK libraries**
    Create `requirements.txt`:
    ```bash
   aws-cdk=2.*
   construct>=10.0.0,<11.0.0
    ```
   then run:
    ```bash
        pip3 install -r requiements.txt
    ```
5. **Bootstrap your environment** (once per region/acccount)
    ```bash
    cdk boostrap aws://<account-id/<region> 
    ```

---

## 📁 Project Structure
```
    my-cdk-app/
    ├── app.py
    ├── cdk.json
    ├── requirements.txt
    └── vpc_stack.py
```

--- 
