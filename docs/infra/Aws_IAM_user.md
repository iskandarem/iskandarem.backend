## Setting Up AWS IAM and CLI

### What is IAM?

IAM stands for **Identity and Access Management**. It’s a tool in AWS that helps you control who can do what. Basically, you use it to create users and give them permission to use AWS services.

---

### Why I Needed It

I needed to use AWS from the terminal (for Terraform and AWS CLI), so I had to create a user that has permission to do things like create resources. This is done through IAM.

---

### Step 1: Create an IAM User

Here’s what I did:

1. Went to the AWS Console → searched for **IAM** and clicked on it.
2. Clicked **"Users"** on the left menu, then clicked **"Add users"**.
3. Gave the user a name (like `terraform-user`).
4. Checked the box for **Programmatic access** (this is what gives you access keys for CLI use).
5. On the permissions screen, I chose **"Attach policies directly"** and picked **AdministratorAccess** just to make things easy for now.
   - This gives full access to everything, which is fine while setting things up.
6. Skipped tags and clicked **Create user**.

---

### Step 2: Get the Access Keys

After the user was created, AWS gave me:

- **Access Key ID**
- **Secret Access Key**

I downloaded the `.csv` file with these credentials and kept it safe. The secret key is only shown once, so make sure to save it.

---

### Step 3: Set Up the AWS CLI

To use AWS from my terminal, I ran this command:

```bash
aws configure
```


After that, it asked me to enter some info:

- Access Key ID: I pasted the one from earlier

- Secret Access Key: I pasted the secret key

- Default region: I used the region from IAM-user

- Output format: I used json