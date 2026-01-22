# Changing Fork via SSH on Comma 3

## Quick Method (Without Factory Reset)

### 1. SSH into your Comma 3
```bash
ssh comma@[YOUR_COMMA_IP]
# Default password: comma
```

### 2. Stop openpilot
```bash
tmux kill-session -t comma
# or
sudo systemctl stop openpilot
```

### 3. Change to your new fork
```bash
cd /data
rm -rf openpilot
git clone -b release-c3 https://github.com/vibhusapra/sunnypilot_polestar.git openpilot
cd openpilot
git submodule update --init --recursive
```

### 4. Restart the device
```bash
sudo reboot
```

## Alternative: Update Existing Installation

If you already have a fork installed and want to switch:

### Option A: Change remote and pull
```bash
cd /data/openpilot
git remote set-url origin https://github.com/vibhusapra/sunnypilot_polestar.git
git fetch origin
git checkout release-c3
git reset --hard origin/release-c3
git submodule update --init --recursive
sudo reboot
```

### Option B: Complete replacement (cleaner)
```bash
cd /data
mv openpilot openpilot_backup
git clone -b release-c3 --depth 1 https://github.com/vibhusapra/sunnypilot_polestar.git openpilot
sudo reboot
```

## Useful SSH Commands

### Check current fork
```bash
cd /data/openpilot
git remote -v
git branch
git log -1
```

### Check if FINGERPRINT is set
```bash
grep FINGERPRINT /data/openpilot/launch_env.sh
```

### Monitor logs
```bash
# Watch real-time logs
tmux attach -t comma

# Check fingerprint detection
grep -i fingerprint /data/log/swaglog.* | tail -10

# Check for errors
grep -i error /data/log/swaglog.* | tail -20
```

### Check car detection
```bash
cat /data/params/d/CarParams | xxd | head -100
# Look for POLESTAR_2 in the output
```

## Troubleshooting via SSH

### If car not recognized
```bash
# Add fingerprint override if missing
echo 'export FINGERPRINT="POLESTAR_2"' >> /data/openpilot/launch_env.sh
sudo reboot
```

### Clear calibration (if needed)
```bash
rm -rf /data/params/d/CalibrationParams
rm -rf /data/params/d/LiveParameters
```

### Force recompile
```bash
cd /data/openpilot
scons -j4
sudo reboot
```

### Check system status
```bash
# Check if openpilot is running
ps aux | grep manager.py

# Check CPU temperature
cat /sys/class/thermal/thermal_zone*/temp

# Check disk space
df -h /data
```

## Quick SSH Script

Save this as `switch_fork.sh` on your Comma 3:

```bash
#!/bin/bash
REPO=$1
BRANCH=$2

if [ -z "$REPO" ] || [ -z "$BRANCH" ]; then
    echo "Usage: ./switch_fork.sh [github_user/repo] [branch]"
    echo "Example: ./switch_fork.sh vibhusapra/sunnypilot_polestar release-c3"
    exit 1
fi

echo "Switching to $REPO branch $BRANCH..."
cd /data
sudo systemctl stop openpilot
rm -rf openpilot_old
mv openpilot openpilot_old 2>/dev/null
git clone -b "$BRANCH" --depth 1 "https://github.com/$REPO.git" openpilot
cd openpilot
git submodule update --init --recursive

echo "Fork switched! Rebooting..."
sudo reboot
```

Then use it:
```bash
chmod +x switch_fork.sh
./switch_fork.sh vibhusapra/sunnypilot_polestar release-c3
```

## SSH Tips

### Keep SSH session alive
Add to your local `~/.ssh/config`:
```
Host comma
    HostName [YOUR_COMMA_IP]
    User comma
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Then connect with:
```bash
ssh comma
```

### Run commands without entering SSH
```bash
ssh comma@[YOUR_COMMA_IP] "cd /data/openpilot && git status"
```

### Copy files to/from Comma
```bash
# Copy from Comma to local
scp comma@[YOUR_COMMA_IP]:/data/log/swaglog.* ./logs/

# Copy to Comma
scp ./custom_file.py comma@[YOUR_COMMA_IP]:/data/openpilot/
```

## For Your Specific Case

After you push to GitHub, SSH in and run:
```bash
cd /data
sudo systemctl stop openpilot
rm -rf openpilot
git clone -b release-c3 https://github.com/vibhusapra/sunnypilot_polestar.git openpilot
sudo reboot
```

That's it! The car will reboot with your Polestar 2 fork.