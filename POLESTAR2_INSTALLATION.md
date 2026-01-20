# Polestar 2 / Volvo CMA Installation Guide for Comma 3

## ✅ Ready to Install!

Your custom sunnypilot fork with Volvo CMA platform support (Polestar 2, XC40 Recharge, C40 Recharge) is now ready to install on your Comma 3.

---

## 🚀 Installer URL

Use this URL to install on your Comma 3:

```
https://smiskol.com/fork/vibhusapra/volvo-cma-polestar2
```

**Alternative installer URL:**
```
https://installer.comma.ai/vibhusapra/sunnypilot/volvo-cma-polestar2
```

---

## 📱 Installation Instructions

### Method 1: Via Comma 3 UI (Easiest)

1. **On your Comma 3**, go to Settings → Device → Uninstall openpilot
2. Wait for the installer screen to appear
3. **Enter custom URL**:
   ```
   https://smiskol.com/fork/vibhusapra/volvo-cma-polestar2
   ```
4. **Wait for installation** (5-10 minutes)
5. Device will reboot automatically

### Method 2: Via SSH

```bash
# SSH to your Comma 3
ssh comma@<comma3_ip>

# Backup existing installation (optional)
cd /data
sudo mv openpilot openpilot.backup

# Clone your fork
git clone -b volvo-cma-polestar2 --recurse-submodules \
  https://github.com/vibhusapra/sunnypilot.git openpilot

# Reboot
cd openpilot
sudo reboot
```

---

## ✅ Post-Installation Verification

After reboot, SSH back in and verify:

```bash
ssh comma@<comma3_ip>

# 1. Check branch
cd /data/openpilot
git branch --show-current
# Expected: volvo-cma-polestar2

# 2. Check commit
git log -1 --oneline
# Expected: "Add Volvo CMA platform support..."

# 3. Verify Volvo models available
python3 -c "from openpilot.selfdrive.car.volvo.values import CAR; print([c.name for c in CAR])"
# Expected: ['VOLVO_XC40_RECHARGE', 'POLESTAR_2', 'VOLVO_S60_RECHARGE']
```

---

## 🎯 What's Included

### Volvo CMA Features

**Steering Control:**
- ✅ Angle-based steering via LCA protocol
- ✅ Asymmetric left/right angle encoding (fixes -4.25° cap)
- ✅ Works with stock ACC

**Safety (from Paper's dev3):**
- ✅ ESC intervention detection
- ✅ LCA_2 checksum fix for stability events
- ✅ Counter management (generates vs forwards)
- ✅ LCA_4 crash fix

**Supported Models:**
- ✅ **Polestar 2** (2020-2024) - CMA platform
- ✅ **Volvo XC40 Recharge** (2021-2023) - CMA platform
- ✅ **Volvo C40 Recharge** (2022+) - CMA platform
- ✅ **Volvo S60 Recharge** (2024) - SPA platform

**UI Toggles:**
- ✅ VolvoDoubleTapCruise (engage on double-tap cruise stalk)
- ✅ VolvoSpoofPAHandsOnWheel (work alongside Pilot Assist)

---

## 🔍 First Boot Checks

**Expected Behavior:**

1. **Without car connected:**
   - Comma 3 boots normally to sunnypilot UI
   - No errors in Settings → Software
   - Volvo models visible in car selector

2. **With car connected (ignition on):**
   - Polestar 2 detected (or "Car unrecognized" if fingerprint doesn't match)
   - No import errors
   - No Python tracebacks

**If you see errors:**
- Check `/data/community/crashes/` for crash logs
- Share error messages for debugging

---

## 🚗 Testing Procedure

**IMPORTANT: Follow POLESTAR2_SETUP.md for complete testing guide!**

### Quick Testing Steps:

1. **Phase 1: Hardware Setup**
   - Wire your harness (MID-1 CAN intercept)
   - Verify connections with multimeter
   - Install harness in car (car off)

2. **Phase 2: Passive Monitoring (First Drive)**
   - Drive with stock Pilot Assist only
   - openpilot logs but doesn't control
   - Verify no dash errors
   - Check logs after drive

3. **Phase 3: Active Steering Test (Parking Lot)**
   - **Empty parking lot only**
   - **Hands on wheel at ALL times**
   - Engage openpilot at low speed (10-20 mph)
   - Test left turn, right turn, straight
   - Verify easy to override

4. **Phase 4: Highway Test (If parking lot successful)**
   - Light traffic, good weather
   - Start on straight highway section
   - **Hands on wheel constantly**
   - Monitor for asymmetry or errors

---

## 📊 Known Differences vs Paper's Fork

| Feature | Paper's v0.10.3 | Your sunnypilot C3 |
|---------|-----------------|-------------------|
| **Base version** | v0.10.3 (3X/C4) | v0.9.8.0 (C3) |
| **Comma 3 support** | ❌ Dropped | ✅ Full support |
| **Volvo steering** | ✅ | ✅ Same code |
| **Safety fixes** | ✅ dev3 | ✅ dev3 (ported) |
| **sunnypilot features** | ❌ | ✅ MADS, DLP, etc. |
| **UI customization** | Paper's custom | sunnypilot UI |

---

## ⚠️ Safety Reminders

**CRITICAL - READ BEFORE TESTING:**

1. **Hands on wheel at ALL times** during initial testing
2. **Start in safe environments** - empty parking lots, then quiet roads
3. **Be ready to disengage** instantly
4. **Driver is always responsible** - SAE Level 2 driver assist
5. **Test incrementally** - don't jump straight to highway
6. **Monitor for errors** - any dash warnings = stop and investigate

**Polestar 2 is UNTESTED** - you're the first person testing this:
- XC40 Recharge is proven working (Paper's car)
- Polestar 2 uses same CMA platform but may have differences
- Start cautiously and report any issues

---

## 🛠️ Troubleshooting

### Installation fails / won't boot

**Check:**
- Comma 3 has enough storage (df -h /data)
- Internet connection stable
- Git clone completed successfully

**Recovery:**
```bash
cd /data
sudo rm -rf openpilot
# Restore backup or install stock sunnypilot
```

### "Car unrecognized" on first connection

**Normal!** The Polestar 2 fingerprint is a placeholder (uses XC40 baseline).

**Solution:**
1. Drive with stock Pilot Assist for 10-30 seconds
2. openpilot will log CAN messages
3. After drive, extract real fingerprint:
   ```bash
   cd /data/openpilot
   python selfdrive/debug/print_docs_diff.py
   ```
4. Update `selfdrive/car/volvo/fingerprints.py` with real Polestar 2 data

### Steering doesn't engage

**Check:**
1. Panda safety mode (should be `volvo`, not `SAFETY_SILENT`)
2. CAN traffic on both CAN0 and CAN2 visible in logs
3. No dash errors (DTC codes)

### Steering feels asymmetric (harder to override right vs left)

**Known issue** from Paper's notes - needs tuning:
- Location: `selfdrive/car/volvo/carcontroller.py`
- May need to adjust torque variable
- Report to sunnypilot Discord for help

---

## 📞 Getting Help

### Resources:

1. **sunnypilot Discord**: https://discord.gg/sunnypilot
   - #comma-three channel for C3-specific issues
   - #development for Volvo-specific questions

2. **This repo issues**: https://github.com/vibhusapra/sunnypilot/issues
   - Report Polestar 2-specific bugs
   - Share fingerprints and logs

3. **Paper's Volvo work**: Reference for comparison
   - His XC40 is proven working
   - Compare your logs with his implementation

### When asking for help, include:

- Comma 3 software version
- Car model and year
- Route ID from problem drive
- Specific error messages
- What you were doing when issue occurred

---

## 🎉 Success Criteria

**Before regular use, verify:**

- ✅ No dash errors during operation
- ✅ Smooth steering on highway
- ✅ Easy driver override (< 10 lb force)
- ✅ Symmetrical left/right behavior
- ✅ Stable for 30+ minute continuous drive
- ✅ No checksum errors in logs

**Once these pass, you have a working Polestar 2 port!**

---

## 📝 What's Next

1. **Capture real Polestar 2 fingerprint** (update fingerprints.py)
2. **Test all features** (double-tap cruise, PA hands-on-wheel spoof)
3. **Tune if needed** (steering feel, override force)
4. **Share your results** with the community!

---

## 🙏 Credits

- **Paper** (@paper5590) - Original Volvo CMA implementation
- **tfife** - Steering improvements in dev3
- **sunnypilot team** - C3 support maintenance
- **Claude Code** - Integration and porting assistance

---

**Good luck with your Polestar 2 port! 🚗⚡**

*Stay safe and enjoy the drive!*
