# 🚀 Vercel Deployment Guide (Alternative to Netlify)

## Why Vercel?
- Made by the Next.js team
- More reliable for Next.js deployments
- No blob storage issues
- 100% free tier

---

## Step 1: Deploy to Vercel

### 1.1 Sign Up & Import Project

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. Click **"Add New..."** → **"Project"**
3. **Import your repository**: `aiversehack01`
4. Vercel will auto-detect Next.js settings:
   - **Framework Preset**: Next.js ✅ (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

### 1.2 Configure Environment Variables

Click **"Environment Variables"** and add:

| Variable Name | Value |
|--------------|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend.onrender.com` |
| `NEXTAUTH_URL` | Leave blank for now |
| `NEXTAUTH_SECRET` | Generate: `openssl rand -base64 32` |
| `GITHUB_ID` | Your GitHub OAuth App Client ID |
| `GITHUB_SECRET` | Your GitHub OAuth App Client Secret |

### 1.3 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Vercel will give you a URL like: `https://your-project.vercel.app`

---

## Step 2: Update Configuration

### 2.1 Update Vercel Environment Variables

1. Go to your project → **Settings** → **Environment Variables**
2. Update `NEXTAUTH_URL` to your actual Vercel URL:
   ```
   https://your-project.vercel.app
   ```
3. Click **"Save"**
4. Go to **Deployments** → Click ⋯ on latest → **"Redeploy"**

### 2.2 Update GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click your OAuth App
3. Update:
   - **Homepage URL**: `https://your-project.vercel.app`
   - **Callback URL**: `https://your-project.vercel.app/api/auth/callback/github`
4. Click **"Update application"**

### 2.3 Update Render Backend CORS

1. Go to **Render Dashboard** → Your backend service
2. **Environment** tab
3. Update `ALLOWED_ORIGINS`:
   ```
   https://your-project.vercel.app,http://localhost:3000
   ```
4. Save (auto-redeploys)

---

## Step 3: Test Your Deployment

1. Visit `https://your-project.vercel.app`
2. Click **"Login with GitHub"**
3. Authorize the app
4. Upload resume and LinkedIn URL
5. Check Supabase → **Table Editor** → `users` table

---

## ✅ Advantages of Vercel over Netlify

| Feature | Vercel | Netlify |
|---------|--------|---------|
| Next.js Support | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐ Plugin |
| Deployment Speed | ~2 min | ~5 min |
| Blob Storage Issues | ✅ None | ❌ Frequent |
| Edge Functions | ✅ Built-in | ⚠️ Limited |
| Free Tier | 100GB bandwidth | 100GB bandwidth |

---

## 🔄 Migration from Netlify

If you already deployed to Netlify, you can keep both or delete the Netlify site:

**To delete Netlify deployment:**
1. Netlify Dashboard → Site settings
2. Scroll to bottom → **"Delete site"**

---

## 📝 Final Checklist

- [ ] Vercel project deployed
- [ ] Environment variables set
- [ ] `NEXTAUTH_URL` updated with Vercel URL
- [ ] GitHub OAuth callback URL updated
- [ ] Render `ALLOWED_ORIGINS` updated
- [ ] Can login with GitHub
- [ ] Can upload resume
- [ ] Data appears in Supabase

---

## 🎉 You're Done!

Your app is now live on:
- **Frontend**: Vercel
- **Backend**: Render  
- **Database**: Supabase

All on **100% free tier**! 🚀
