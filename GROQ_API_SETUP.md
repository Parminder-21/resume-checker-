# Groq API Integration - Setup Guide

## ✅ What Changed

Your application now uses **Groq API** (FREE & UNLIMITED) instead of Anthropic Claude API.

### Changes Made:
1. ✅ Updated `requirements.txt` - replaced `anthropic` with `groq`
2. ✅ Updated `.env` - changed to use `GROQ_API_KEY` instead of `ANTHROPIC_API_KEY`
3. ✅ Updated `config.py` - configured to load Groq API key
4. ✅ Updated `resume_rewriter.py` - now uses Groq client instead of Anthropic

---

## 🚀 Step 1: Get Your Free Groq API Key

### Option A: Quick Setup (Recommended)
1. Go to: **https://console.groq.com**
2. Click **"Sign Up"** (takes 30 seconds)
3. Use email or GitHub to register
4. Verify your email if needed
5. Click **"API Keys"** in the left sidebar
6. Click **"Create API Key"**
7. Copy your key (starts with `gsk_`)
8. Save it somewhere safe

### Option B: If you already have a Groq account
1. Go to: https://console.groq.com/keys
2. Create a new API key
3. Copy it

---

## 🔧 Step 2: Add Your API Key to .env File

### Open `.env` file:
```
c:\Users\abc\OneDrive\Desktop\resume checker\backend\.env
```

### Find this line:
```
GROQ_API_KEY=gsk_your-groq-api-key-here
```

### Replace with your actual key:
```
GROQ_API_KEY=gsk_YOUR_ACTUAL_KEY_HERE
```

**Example:**
```
GROQ_API_KEY=gsk_abc123def456ghi789jkl
```

Save the file (Ctrl+S).

---

## 📥 Step 3: Install Updated Dependencies

Open PowerShell in your backend folder and run:

```powershell
cd backend
pip install -r requirements.txt
```

This will:
- Remove `anthropic` package
- Install `groq` package (free client library)

---

## ▶️ Step 4: Run Your Application

### Start Backend:
```powershell
cd backend
python run.py
```

Or use:
```powershell
START.bat
```

### Start Frontend:
```powershell
cd frontend
npm run dev
```

Or use:
```powershell
START.bat
```

---

## ✨ Benefits of Groq API

| Feature | Groq | Anthropic |
|---------|------|-----------|
| **Cost** | 🆓 FREE (unlimited) | 💰 Expensive (~$0.015/1K tokens) |
| **Speed** | 🚀 Ultra fast (50x faster) | ⚡ Fast |
| **Quality** | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Best-in-class |
| **Models** | Mixtral, Llama | Claude 3 |
| **API Key Setup** | ⭐ Easy | ⭐ Easy |

---

## 🧪 Test Your Setup

After everything is running, test these flows:

1. Upload a resume PDF
2. Paste a job description
3. Click "Optimize Resume"
4. ✅ Should see rewritten bullets in seconds
5. Download the optimized PDF

If you see results, **Groq API is working!** 🎉

---

## 🆘 Troubleshooting

### Error: "GROQ_API_KEY not found"
- Check your `.env` file has the line: `GROQ_API_KEY=gsk_...`
- Restart the backend server after editing `.env`

### Error: "Invalid API key"
- Make sure you copied the full key from console.groq.com
- Check for extra spaces or quotes

### Error: "Rate limited"
- You might have hit the free tier limits (unlikely for one user)
- Contact Groq support - they're very responsive

### Slow responses
- This shouldn't happen with Groq - it's very fast
- Check your internet connection
- The first request might take a bit longer

---

## 📊 Groq Models Available (All Free)

```
1. mixtral-8x7b-32768    ← Recommended (best quality/speed)
2. llama2-70b-4096       ← High quality, slower
3. llama-2-7b-chat       ← Very fast, lower quality
```

Your app uses `mixtral-8x7b-32768` by default (perfect for resume rewriting).

---

## 💡 Next Steps

1. Get your Groq API key from https://console.groq.com
2. Update `.env` with your key
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app and test!

**That's it!** Your resume optimizer is now powered by free, fast Groq API! 🚀

---

## 📞 Support

- **Groq Issues**: https://support.groq.com
- **Groq Discord**: https://discord.gg/groq
- **API Docs**: https://console.groq.com/docs
