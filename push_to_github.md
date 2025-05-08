# Instructions for Pushing to GitHub

Follow these steps to push your AI Prompt Database to GitHub:

## 1. Create a GitHub Personal Access Token (PAT)

1. Go to GitHub: https://github.com/settings/tokens
2. Click "Generate new token" (classic)
3. Give it a name like "AI Prompt DB"
4. Select the "repo" scope
5. Click "Generate token"
6. Copy the token (you'll only see it once)

## 2. Push to GitHub

Run the following commands in your terminal:

```bash
# Configure Git with your GitHub username and email
git config --global user.name "YourGitHubUsername"
git config --global user.email "your.email@example.com"

# Add the remote repository (if not already added)
git remote add origin https://github.com/GRsoldier7/AI_Prompt_DB.git

# Push to GitHub (you'll be prompted for your username and PAT)
git push -u origin master
```

When prompted for your password, use the Personal Access Token you created.

## 3. Verify the Repository

1. Go to https://github.com/GRsoldier7/AI_Prompt_DB
2. Verify that all your files have been pushed successfully

## 4. Future Updates

For future updates, use these commands:

```bash
# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push changes
git push
```
