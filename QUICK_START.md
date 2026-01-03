# Quick Start Guide - Operations & Monitoring System

## 🚀 Quick Setup (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create test users
python setup_db.py

# 3. Start the app
python app.py
```

**Access**: Open browser → `http://localhost:5000`

---

## 🔑 Test Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Technician | `technician1` | `password123` |
| Engineer | `engineer1` | `password123` |
| DM | `dm1` | `password123` |
| DGM | `dgm1` | `password123` |

---

## 📋 Role-Based Quick Tasks

### 👷 TECHNICIAN
1. **Daily Monitoring** → Forms → Daily Monitoring
2. **Report Fault** → From dashboard
3. **View Equipment** → Forms → Equipment Status
4. **Data Re-verification** → Forms → Data Re-verification
5. **Performance Report** → Forms → Performance Report

### 👨‍💻 ENGINEER
1. **Investigate Faults** → Dashboard → View Pending Faults
2. **Root Cause Analysis** → Forms → Root Cause Analysis
3. **Create Resolution** → Forms → Draft Resolution
4. **Documentation Package** → Forms → Documentation Package
5. **Technical Reference** → Forms → Technical Reference
6. **Delivery Verification** → Forms → Delivery Verification
7. **Vendor Management** → Forms → Vendor Management

### 👔 DM (Deputy Manager)
1. **Approve Reports** → Dashboard → Pending Reports
2. **Review Reports** → Views → Report Review
3. **Historical Data** → Views → Historical Data
4. **Trend Comparison** → Views → Trend Comparison

### 👑 DGM (Deputy General Manager)
1. **Everything DM can do** +
2. **Verify Deliveries** → Review pending verifications
3. **View Archives** → Reports → Approved Reports
4. **System Oversight** → All dashboards and analytics

---

## 🔄 Common Workflows

### Fault Resolution Flow
```
Technician Reports Fault
    ↓
Engineer Performs RCA
    ↓
Engineer Creates Resolution Report
    ↓
DM Approves Report
    ↓
Fault Resolved ✅
```

### Performance Report Flow
```
Technician Creates Report
    ↓
Technician Submits for Approval
    ↓
DM Reviews & Approves
    ↓
Report Archived ✅
```

### Delivery Verification Flow
```
Engineer Creates Verification
    ↓
DGM Verifies
    ↓
Verification Complete ✅
```

---

## 📍 Key URLs

### Dashboards
- Technician: `/dashboard/technician`
- Engineer: `/dashboard/engineer`
- DM: `/dashboard/dm`
- DGM: `/dashboard/dgm`

### Forms
- Daily Monitoring: `/forms/daily-monitoring`
- Root Cause Analysis: `/forms/root-cause-analysis`
- Draft Resolution: `/forms/draft-resolution`
- Documentation Package: `/forms/documentation-package`
- Technical Reference: `/forms/technical-reference`
- Delivery Verification: `/forms/delivery-verification`
- Vendor Management: `/forms/vendor-management`
- Data Re-verification: `/forms/data-reverification`
- Performance Report: `/forms/performance-report`
- Equipment Status: `/forms/equipment-status`

### Views
- Monitoring History: `/views/monitoring-history`
- Fault List: `/views/fault-list`
- Report Review: `/views/report-review`
- Historical Data: `/views/historical-data`
- Trend Comparison: `/views/trend-comparison`
- Escalation Timeline: `/views/escalation-timeline`

---

## 🔔 Quick Tips

1. **Always check notifications** (bell icon 🔔)
2. **Save drafts** before submitting
3. **Use equipment codes** for easy reference
4. **Fill all required fields** (marked with *)
5. **Logout** when done for security

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't login | Run `python setup_db.py` to create users |
| Database error | Run `python app.py` to create database |
| Port 5000 in use | Change port in `app.py` line 9 |
| Forms not loading | Clear browser cache, check login |

---

**For detailed guide**: See `COMPLETE_USER_GUIDE.md`




