# PyPI API Token Setup

## How to set up your PyPI API token:

1. **Create a PyPI account** at https://pypi.org/account/register/
2. **Generate an API token**:
   - Go to https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Name: "sproclib-upload" (or any name you prefer)
   - Scope: Select "Entire account" or specific to "sproclib" project
   - Click "Add token"

3. **Create the token file**:
   ```bash
   # Copy your token (starts with pypi-...) and save it to:
   echo "pypi-your-actual-token-here" > scripts/pypi/api-token.txt
   ```

4. **For TestPyPI** (optional, for testing):
   - Create account at https://test.pypi.org/account/register/
   - Generate token at https://test.pypi.org/manage/account/token/
   - Use the same `api-token.txt` file (the script will try both)

## Security Notes:

⚠️ **IMPORTANT**: 
- Never commit `api-token.txt` to git
- This file is already in `.gitignore`
- Keep your token private and secure
- Regenerate tokens if compromised

## Usage:

Once you have created `scripts/pypi/api-token.txt` with your token:

```bash
# Build and upload automatically
./scripts/pypi/build_and_upload.sh --upload

# Or upload existing build
./scripts/pypi/upload_only.sh
```

The scripts will automatically use your token for authentication.
