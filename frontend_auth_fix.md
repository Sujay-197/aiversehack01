
# Missing Environment Variables

The "Server Error" during login is usually caused by missing authentication secrets. NextAuth requires these to be set in a `.env` file in the **frontend** directory.

### 1. Create a `.env` file
Create a file at `frontend/.env` with the following content:

```env
# REQUIRED for NextAuth v5
AUTH_GITHUB_ID=your_github_client_id
AUTH_GITHUB_SECRET=your_github_client_secret
AUTH_SECRET=your_random_auth_secret # Generate with: openssl rand -base64 33

# Optional but recommended
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Update GitHub OAuth Settings
Ensure your GitHub OAuth App has:
- **Homepage URL**: `http://localhost:3000`
- **Authorization callback URL**: `http://localhost:3000/api/auth/callback/github`
