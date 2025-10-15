# How to Save sritpop to your terminal

Complete guide to make your terminal system monitor easily accessible from your zsh shell.

---

## Table of Contents

- [Method 1: Create an Alias (Recommended)](#method-1-create-an-alias-recommended)
- [Method 2: Add to PATH](#method-2-add-to-path)
- [Method 3: Create a Function](#method-3-create-a-function)
- [Method 4: System-Wide Installation](#method-4-system-wide-installation)
- [Bonus: Oh My Zsh Plugin](#bonus-oh-my-zsh-plugin)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Uninstalling](#uninstalling)

---

## Method 1: Create an Alias (Recommended)

**Best for:** Most users, quick setup, easy to manage

### Step-by-Step

#### 1. Find your project's full path

```bash
cd ~/terminal-monitor
pwd
```

Copy the output (e.g., `/home/username/terminal-monitor`)

#### 2. Open your zsh configuration

```bash
nano ~/.zshrc
```

#### 3. Add the alias at the end of the file

```bash
# Terminal System Monitor
alias sysmon='python3 /home/username/terminal-monitor/monitor.py'
```

Replace `/home/username/terminal-monitor` with your actual path from step 1.

#### 4. Save and exit

- Press `Ctrl + O` to save
- Press `Enter` to confirm
- Press `Ctrl + X` to exit

#### 5. Reload your zsh configuration

```bash
source ~/.zshrc
```

#### 6. Test it!

```bash
sysmon
```

### Quick One-Liner Setup

If you're in the `terminal-monitor` directory:

```bash
echo "alias sysmon='python3 $(pwd)/monitor.py'" >> ~/.zshrc
source ~/.zshrc
```

This automatically adds the alias with the correct path!

### Pros & Cons

✅ **Pros:**
- Very simple
- Easy to modify
- No file copying needed
- Quick setup

❌ **Cons:**
- Requires full path
- Only works for your user

---

## Method 2: Add to PATH

**Best for:** More professional setup, works like native commands

### Step-by-Step

#### 1. Create a bin directory

```bash
mkdir -p ~/bin
```

#### 2. Copy or link the script

**Option A: Copy (simpler)**
```bash
cp ~/terminal-monitor/monitor.py ~/bin/sysmon
```

**Option B: Symbolic link (better for updates)**
```bash
ln -s ~/terminal-monitor/monitor.py ~/bin/sysmon
```

#### 3. Make it executable

```bash
chmod +x ~/bin/sysmon
```

#### 4. Add ~/bin to your PATH

Open ~/.zshrc:
```bash
nano ~/.zshrc
```

Add this line at the end:
```bash
# Add personal bin to PATH
export PATH="$HOME/bin:$PATH"
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

#### 5. Reload zsh

```bash
source ~/.zshrc
```

#### 6. Test from anywhere

```bash
cd ~
sysmon
```

### Pros & Cons

✅ **Pros:**
- Works like a native command
- Clean and professional
- No alias needed
- Can be versioned

❌ **Cons:**
- Slightly more complex
- Requires PATH modification

---

## Method 3: Create a Function

**Best for:** Advanced users, need to activate virtual environment automatically

### Step-by-Step

#### 1. Open ~/.zshrc

```bash
nano ~/.zshrc
```

#### 2. Add this function

```bash
# Terminal System Monitor
sysmon() {
    # Save current directory
    local current_dir=$(pwd)
    
    # Navigate to project directory
    cd ~/terminal-monitor
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Run the monitor
    python3 monitor.py
    
    # Deactivate virtual environment
    if [ -d "venv" ]; then
        deactivate
    fi
    
    # Return to original directory
    cd "$current_dir"
}
```

#### 3. Save and reload

```bash
# Save (Ctrl+O, Enter, Ctrl+X)
source ~/.zshrc
```

#### 4. Run it

```bash
sysmon
```

### Pros & Cons

✅ **Pros:**
- Handles virtual environment automatically
- Returns to original directory
- Can add custom logic
- Most flexible

❌ **Cons:**
- More complex
- Overkill for simple use

---

## Method 4: System-Wide Installation

**Best for:** Multi-user systems, production environments

### Step-by-Step

#### 1. Install dependencies system-wide

```bash
sudo pip3 install textual psutil
```

Or use your package manager if available:
```bash
# Ubuntu/Debian
sudo apt install python3-textual python3-psutil
```

#### 2. Copy script to system bin

```bash
sudo cp ~/terminal-monitor/monitor.py /usr/local/bin/sysmon
```

#### 3. Make it executable

```bash
sudo chmod +x /usr/local/bin/sysmon
```

#### 4. Test it

```bash
sysmon
```

This works for ALL users on the system!

### Pros & Cons

✅ **Pros:**
- Available to all users
- No PATH or alias needed
- Professional installation
- Works like native tools

❌ **Cons:**
- Requires root/sudo
- System-wide dependencies
- Updates need sudo
- Can affect other users

---

## Bonus: Oh My Zsh Plugin

**Best for:** Oh My Zsh users who want organized plugins

### Step-by-Step

#### 1. Create plugin directory

```bash
mkdir -p ~/.oh-my-zsh/custom/plugins/sysmon
```

#### 2. Create plugin file

```bash
nano ~/.oh-my-zsh/custom/plugins/sysmon/sysmon.plugin.zsh
```

#### 3. Add plugin content

```bash
# System Monitor Plugin
# Provides easy access to terminal system monitor

# Main alias
alias sysmon='python3 ~/terminal-monitor/monitor.py'

# Alternative with sudo for full access
alias sysmon-sudo='sudo python3 ~/terminal-monitor/monitor.py'

# Function version with venv support
sysmon-venv() {
    cd ~/terminal-monitor
    source venv/bin/activate
    python3 monitor.py
    deactivate
}
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

#### 4. Enable the plugin

Edit ~/.zshrc:
```bash
nano ~/.zshrc
```

Find the `plugins=()` line and add `sysmon`:
```bash
plugins=(
    git
    zsh-autosuggestions
    sysmon
)
```

#### 5. Reload zsh

```bash
source ~/.zshrc
```

#### 6. Use it

```bash
sysmon              # Normal mode
sysmon-sudo         # With sudo for all processes
sysmon-venv         # Using virtual environment
```

### Pros & Cons

✅ **Pros:**
- Organized and clean
- Multiple command variants
- Easy to share/version control
- Follows Oh My Zsh conventions

❌ **Cons:**
- Only for Oh My Zsh users
- More setup required

---

## Verification

After setting up, verify everything works:

### Test 1: Check if command is available

```bash
which sysmon
# Should show path or alias info
```

### Test 2: Run from home directory

```bash
cd ~
sysmon
# Should start the monitor
```

### Test 3: Check alias/function

```bash
alias | grep sysmon
# or
type sysmon
```

Expected output examples:
```bash
# For alias:
sysmon='python3 /home/username/terminal-monitor/monitor.py'

# For function:
sysmon is a shell function

# For PATH method:
sysmon is /home/username/bin/sysmon
```

---

## Troubleshooting

### Issue: "command not found: sysmon"

**Solution 1:** Reload zsh configuration
```bash
source ~/.zshrc
```

**Solution 2:** Check if alias exists
```bash
cat ~/.zshrc | grep sysmon
```

**Solution 3:** Start a new terminal session
```bash
exec zsh
```

### Issue: "Permission denied"

**Solution:** Make script executable
```bash
chmod +x ~/terminal-monitor/monitor.py
# or
chmod +x ~/bin/sysmon
```

### Issue: "No module named 'textual'"

**Solution:** Activate virtual environment or install packages
```bash
cd ~/terminal-monitor
source venv/bin/activate
# or
pip install textual psutil
```

### Issue: PATH method not working

**Solution:** Check if ~/bin is in PATH
```bash
echo $PATH | grep -o "$HOME/bin"
```

If empty, add to ~/.zshrc:
```bash
export PATH="$HOME/bin:$PATH"
source ~/.zshrc
```

### Issue: Alias not persisting after restart

**Solution:** Make sure you edited ~/.zshrc (not ~/.bashrc)
```bash
# Check which shell you're using
echo $SHELL
# Should show /bin/zsh or similar

# Verify zshrc is being loaded
echo "export TEST_VAR=123" >> ~/.zshrc
source ~/.zshrc
echo $TEST_VAR
# Should show 123
```

---

## Uninstalling

### Remove Alias Method

```bash
# Edit ~/.zshrc
nano ~/.zshrc

# Delete the line with 'alias sysmon='
# Save and exit

# Reload
source ~/.zshrc
```

### Remove PATH Method

```bash
# Remove the script
rm ~/bin/sysmon

# Optionally remove from PATH in ~/.zshrc
nano ~/.zshrc
# Remove or comment out: export PATH="$HOME/bin:$PATH"
```

### Remove Function Method

```bash
# Edit ~/.zshrc
nano ~/.zshrc

# Delete the entire sysmon() { ... } block
# Save and exit

# Reload
source ~/.zshrc
```

### Remove System-Wide Installation

```bash
sudo rm /usr/local/bin/sysmon
```

### Remove Oh My Zsh Plugin

```bash
# Remove plugin directory
rm -rf ~/.oh-my-zsh/custom/plugins/sysmon

# Edit ~/.zshrc and remove 'sysmon' from plugins array
nano ~/.zshrc

# Reload
source ~/.zshrc
```

---

## Comparison Table

| Method | Difficulty | Scope | Pros | Best For |
|--------|-----------|-------|------|----------|
| **Alias** | ⭐ Easy | User only | Simple, quick | Most users |
| **PATH** | ⭐⭐ Medium | User only | Professional, clean | Power users |
| **Function** | ⭐⭐⭐ Advanced | User only | Most flexible | Developers |
| **System-Wide** | ⭐⭐⭐ Advanced | All users | Like native command | Servers/Multi-user |
| **Oh My Zsh** | ⭐⭐ Medium | User only | Organized | Oh My Zsh users |

---

## Recommended Method

**For beginners:** Start with **Method 1 (Alias)**
```bash
echo "alias sysmon='python3 $(pwd)/monitor.py'" >> ~/.zshrc
source ~/.zshrc
```

**For regular users:** Use **Method 2 (PATH)**
- More professional
- Works like native commands
- Easy to manage

**For developers:** Use **Method 3 (Function)**
- Handles virtual environments
- Most control and flexibility

---

## Additional Tips

### Create Multiple Aliases

You can create shortcuts for different options:

```bash
# In ~/.zshrc
alias sysmon='python3 ~/terminal-monitor/monitor.py'
alias sysmon-sudo='sudo python3 ~/terminal-monitor/monitor.py'
alias sysmon-update='cd ~/terminal-monitor && git pull && pip install -r requirements.txt'
```

### Auto-start on Terminal Open

Add to the end of ~/.zshrc if you want it to start automatically:
```bash
# Auto-start system monitor (comment out if annoying)
# sysmon
```

### Add Keyboard Shortcut

In your terminal emulator settings, add a custom keyboard shortcut:
- Command: `python3 ~/terminal-monitor/monitor.py`
- Shortcut: `Ctrl+Alt+M` (or your preference)

---

## Support

If you encounter issues:

1. Check you're using zsh: `echo $SHELL`
2. Verify file paths: `ls ~/terminal-monitor/monitor.py`
3. Test Python script directly: `python3 ~/terminal-monitor/monitor.py`
4. Check for typos in ~/.zshrc: `cat ~/.zshrc | grep sysmon`

---

**Happy Monitoring! 🚀**

Last updated: October 2025
