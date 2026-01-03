# How to Run setup_environment.bat - Quick Guide

## 🖱️ Method 1: Double-Click (Easiest)

1. **Open File Explorer**
   - Press `Win + E` or open from Start Menu

2. **Navigate to project folder:**
   ```
   C:\Users\S A Z\Desktop\NEW JUNIORS PROJECT
   ```

3. **Find the file:**
   - Look for `setup_environment.bat`

4. **Double-click it**
   - A black Command Prompt window will open
   - The script will run automatically
   - Wait for it to complete (it will show progress messages)
   - Press any key when it says "Press any key to continue..."

---

## ⌨️ Method 2: From Command Prompt

1. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to project folder:**
   ```cmd
   cd "C:\Users\S A Z\Desktop\NEW JUNIORS PROJECT"
   ```

3. **Run the script:**
   ```cmd
   setup_environment.bat
   ```
   or
   ```cmd
   .\setup_environment.bat
   ```

---

## 💻 Method 3: From PowerShell

1. **Open PowerShell:**
   - Press `Win + X` and select "Windows PowerShell"
   - Or search for "PowerShell" in Start Menu

2. **Navigate to project folder:**
   ```powershell
   cd "C:\Users\S A Z\Desktop\NEW JUNIORS PROJECT"
   ```

3. **Run the script:**
   ```powershell
   .\setup_environment.bat
   ```
   or
   ```powershell
   setup_environment.bat
   ```

---

## 🔧 Method 4: From Current Directory (If you're already in the project folder)

If you're already in the project folder in your terminal:

**Command Prompt:**
```cmd
setup_environment.bat
```

**PowerShell:**
```powershell
.\setup_environment.bat
```

---

## ⚠️ If You Get "Execution Policy" Error in PowerShell

If PowerShell shows an error about execution policy:

**Option 1: Run with bypass**
```powershell
powershell -ExecutionPolicy Bypass -File .\setup_environment.bat
```

**Option 2: Change execution policy (one-time)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run:
```powershell
.\setup_environment.bat
```

---

## 📋 What the Script Does

The script will:
1. ✅ Check if Python is installed
2. ✅ Check if pip is available
3. ✅ Create a virtual environment (folder named `venv`)
4. ✅ Activate the virtual environment
5. ✅ Upgrade pip to latest version
6. ✅ Install all dependencies from `requirements.txt`

**Time:** Usually takes 1-3 minutes depending on your internet speed.

---

## ✅ After Running the Script

Once the script completes successfully:

1. **The virtual environment will be activated automatically**

2. **To run the APDS application:**
   ```cmd
   python app.py
   ```

3. **If you close the terminal and want to run the app later:**
   - Open Command Prompt/PowerShell in the project folder
   - Activate virtual environment:
     ```cmd
     venv\Scripts\activate
     ```
   - Run the app:
     ```cmd
     python app.py
     ```

---

## 🆘 Troubleshooting

### Script closes immediately:
- **Solution:** Open Command Prompt first, then navigate to folder and run the script
- Or add `pause` at the end of the script

### "Python is not recognized":
- **Solution:** Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

### "Access is denied":
- **Solution:** Right-click the .bat file → "Run as administrator"

### Script runs but shows errors:
- Check the error message
- See `INSTALLATION_TROUBLESHOOTING.md` for detailed solutions

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| Run script (double-click) | Double-click `setup_environment.bat` |
| Run from CMD | `setup_environment.bat` |
| Run from PowerShell | `.\setup_environment.bat` |
| Activate venv later | `venv\Scripts\activate` |
| Run application | `python app.py` |

---

## 💡 Pro Tip

You can also create a shortcut:
1. Right-click `setup_environment.bat`
2. Select "Create shortcut"
3. Place shortcut on Desktop for easy access

