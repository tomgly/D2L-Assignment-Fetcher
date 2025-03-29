# 📚 Sinclair D2L Assignment Fetcher

This project fetches upcoming assignments and quizzes from Sinclair Community College's D2L (Brightspace) system using D2L's OAuth2.0 authentication.

## Features

- Automatically obtains and refreshes OAuth2 token using browser session cookies
- Lists assignments and quizzes for the next two weeks
- Supports multiple courses
- Outputs details including name, due date, points, and description

## ⚠️ Disclaimer

This project uses cookie-based authentication to access Sinclair's D2L system.

- **Access token lifetime:** ~60 minutes
- **Cookie lifetime:** Typically valid for 1 day
- **Why cookie-based auth?** As a student, you cannot obtain permanent API keys. Instead, cookie values and the CSRF token are extracted from your browser via developer tools (Network tab).

> **Use at your own risk.** Do not publish `.env` or token data. This tool is provided for personal use and learning purposes only.

## 🔧 Setup

### 1. Download the ZIP (for non-developers)

You can download a ready-to-use ZIP package from the [Releases](https://github.com/tomgly/D2L-Assignment-Fetcher/releases) page

1. Go to **Releases** tab
2. Download the latest `Source code (zip)`
3. Extract the ZIP file to any folder

Alternatively (for developers), you can clone the repo

```bash
git clone https://github.com/tomgly/D2L-Assignment-Fetcher.git
cd D2L-Assignment-Fetcher
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

### 3. Create .env file
Create a `.env` file in the root directory with the following contents (get these from browser dev tools while logged in)

```ini
D2L_SESSION_VAL=your_d2lSessionVal
D2L_SECURE_SESSION_VAL=your_d2lSecureSessionVal
X_CSRF_TOKEN=your_x_csrf_token
```

### 4. Configure courses and user ID
Edit `config.json` to include your D2L user ID and the list of course IDs and names

```json
{
  "user_id": "12345",
  "courses": [
    {"id": 384527, "name": "IOT FUNDAMENTALS"},
    {"id": 385942, "name": "JAVA SOFTWARE DEV I"}
  ]
}
```

## 🚀 Usage
To fetch your assignments

```bash
python get_assignments.py
```

If your token is expired or missing, the script will automatically obtain a new one.

## 📁 File Structure

- [`get_assignments.py`](get_assignments.py): Main script to fetch assignments
- [`d2l_oauth2.py`](d2l_oauth2.py): Script to get the OAuth2 token from browser session
- `token.json`: Stores the current access token (automatic generate)
- [`config.json`](config.json): Stores course and user information
- [`.env`](example.env): Stores secure cookie values and CSRF token

## 🔐 Security

- `.env` is excluded from version control by default (`.gitignore`)
- Do not share `.env`, `token.json`, or any cookie values publicly

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## 🔗 References
This method is based on research and findings from the following source

- [Brightspace API Reference](https://docs.valence.desire2learn.com/reference.html)