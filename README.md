

# :computer: Sritop - A Resource monitor

<img width="1350" height="743" alt="Screenshot from 2025-10-15 14-48-06" src="https://github.com/user-attachments/assets/35d4ff04-c577-4a78-9f19-4071c3619180" />


### A beautiful, real-time system monitoring application for your terminal - similar to BTOP/HTOP but built with Python and Textual.


## Setup sritop
### clone the project

```bash
git clone https://github.com/Dulmin2021/sritop.git
cd sritop
pip install -r requirements.txt

```

## How to Save sritop to your terminal

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
alias sysmon='python3 /home/username/sritop/monitor.py'
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


<img width="841" height="562" alt="Screenshot from 2025-10-15 14-46-54" src="https://github.com/user-attachments/assets/be1a3c7c-7ba1-4338-886e-ef638c93d2fb" />



This automatically adds the alias with the correct path!

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
sritop() {
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
sritop
```


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
sudo cp ~/terminal-monitor/monitor.py /usr/local/bin/sritop
```

#### 3. Make it executable

```bash
sudo chmod +x /usr/local/bin/sritop
```

#### 4. Test it

```bash
sritop
```

This works for ALL users on the system!



## Bonus: Oh My Zsh Plugin

**Best for:** Oh My Zsh users who want organized plugins

### Step-by-Step

#### 1. Create plugin directory

```bash
mkdir -p ~/.oh-my-zsh/custom/plugins/sritop
```

#### 2. Create plugin file

```bash
nano ~/.oh-my-zsh/custom/plugins/sysmon/sysmon.sritop.zsh
```

#### 3. Add plugin content

```bash
# System Monitor Plugin
# Provides easy access to terminal system monitor

# Main alias
alias sritop='python3 ~/sritop/monitor.py'

# Alternative with sudo for full access
alias sritop-sudo='sudo python3 ~/sritop/monitor.py'

# Function version with venv support
sysmon-venv() {
    cd ~/sritop
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
    sritop
)
```

#### 5. Reload zsh

```bash
source ~/.zshrc
```

#### 6. Use it

```bash
sritop              # Normal mode
sritop-sudo         # With sudo for all processes
sritop-venv         # Using virtual environment
```

---

## Verification

After setting up, verify everything works:

### Test 1: Check if command is available

```bash
which sritop
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
alias | grep sritop
# or
type sritop
```

Expected output examples:
```bash
# For alias:
sritop='python3 /home/username/sritop/monitor.py'

# For function:
sysmon is a shell function

# For PATH method:
sysmon is /home/username/bin/sritop
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
cat ~/.zshrc | grep sritop
```

**Solution 3:** Start a new terminal session
```bash
exec zsh
```

### Issue: "Permission denied"

**Solution:** Make script executable
```bash
chmod +x ~/sritop/monitor.py
# or
chmod +x ~/bin/sritop
```

### Issue: "No module named 'textual'"

**Solution:** Activate virtual environment or install packages
```bash
cd ~/sritop
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
rm ~/bin/sritop

# Optionally remove from PATH in ~/.zshrc
nano ~/.zshrc
# Remove or comment out: export PATH="$HOME/bin:$PATH"
```

### Remove Function Method

```bash
# Edit ~/.zshrc
nano ~/.zshrc

# Delete the entire sritop() { ... } block
# Save and exit

# Reload
source ~/.zshrc
```

### Remove System-Wide Installation

```bash
sudo rm /usr/local/bin/sritop
```

### Remove Oh My Zsh Plugin

```bash
# Remove plugin directory
rm -rf ~/.oh-my-zsh/custom/plugins/sritop

# Edit ~/.zshrc and remove 'sysmon' from plugins array
nano ~/.zshrc

# Reload
source ~/.zshrc
```
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
