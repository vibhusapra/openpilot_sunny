# Polestar 2 on Comma 3 - Installation Guide

## Status: READY TO INSTALL ✅

Your modified sunnypilot with Polestar 2 support is ready!

## Quick Installation

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Name: `sunnypilot_polestar`
3. Make it PUBLIC (required for Comma to access)
4. DON'T initialize with README
5. Click "Create repository"

### Step 2: Push Code
Run these commands:
```bash
cd /Users/vibhusapra/projects/sunnypilot_polestar_c3
git remote remove myrepo  # Remove if exists
git remote add myrepo https://github.com/vibhusapra/sunnypilot_polestar.git
git push myrepo release-c3
```

### Step 3: Install on Comma 3
1. Factory reset your Comma 3:
   - Settings → Device → Factory Reset
   - OR tap rapidly during boot and select reset

2. When prompted, choose "Custom Software"

3. Enter this URL (NO https://):
   ```
   github.com/vibhusapra/sunnypilot_polestar/release-c3
   ```

4. Wait for installation (10-15 minutes)

## What's Included

✅ Sunnypilot release-c3 (Comma 3 compatible)
✅ Paper's Volvo implementation (master-cma-dev3)
✅ tfife's steering angle fixes (full lock-to-lock)
✅ FINGERPRINT="POLESTAR_2" override
✅ All necessary DBC files

## Testing Checklist

### Before First Drive
- [ ] Verify harness connections (MID 1 CAN)
- [ ] Check IGN wire to VCU1
- [ ] Clear any existing DTCs

### First Start
- [ ] Car recognized as POLESTAR_2
- [ ] No error messages
- [ ] Dashcam view working

### Parking Lot Test
- [ ] Steering engages when cruise enabled
- [ ] Left steering works
- [ ] Right steering works (no -4.25° limit)
- [ ] Driver override works

### Highway Test
- [ ] Stable lane keeping
- [ ] Smooth steering control
- [ ] Stock ACC working

## Troubleshooting

### Car Not Recognized
```bash
# SSH into Comma 3
ssh comma@[device-ip]
cd /data/openpilot
grep FINGERPRINT launch_env.sh  # Should show POLESTAR_2
```

### Check Logs
```bash
grep fingerprint /data/log/swaglog.* | tail -5
```

### Verify Volvo Files
```bash
ls -la selfdrive/car/volvo/
ls -la opendbc/dbc/volvo*
```

## Known Limitations
- No blinker detection (FlexRay)
- City driving: steering rotation speed limited
- ~0.5 km/h speed deviation
- Occasional checksum errors (rare)

## Support

Discord: Paper's thread in comma.ai server
- Paper: Main developer
- tfife: Steering fixes
- evi1gasm: Harness help

## Next Steps After Success

1. Report success in Discord thread
2. Share any issues encountered
3. Consider contributing improvements

---
Generated: $(date)
Branch: release-c3 + Paper's Volvo
Comma 3 Compatible ✅