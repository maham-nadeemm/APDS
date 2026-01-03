# Complete User Guide - Operations & Monitoring System
## From Login to End - Full Workflow

---

## 📋 Table of Contents
1. [Initial Setup](#initial-setup)
2. [Starting the Application](#starting-the-application)
3. [Login Process](#login-process)
4. [Technician Workflow](#technician-workflow)
5. [Engineer Workflow](#engineer-workflow)
6. [DM (Deputy Manager) Workflow](#dm-deputy-manager-workflow)
7. [DGM (Deputy General Manager) Workflow](#dgm-deputy-general-manager-workflow)
8. [Complete Workflow Examples](#complete-workflow-examples)

---

## 🚀 Initial Setup

### Step 1: Install Dependencies
```bash
cd "C:\Users\S A Z\Desktop\NEW JUNIORS PROJECT"
pip install -r requirements.txt
```

### Step 2: Setup Database and Create Test Users
```bash
python setup_db.py
```

This will create test users:
- **technician1** (password: password123)
- **engineer1** (password: password123)
- **dm1** (password: password123)
- **dgm1** (password: password123)

### Step 3: Start the Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 🔐 Login Process

### Accessing the Login Page
1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You'll be redirected to the login page (`/auth/login`)

### Logging In
1. **Enter Username**: Use one of the test accounts (e.g., `technician1`)
2. **Enter Password**: Use `password123`
3. **Click "Login"**
4. You'll be automatically redirected to your role-specific dashboard

### Available Test Accounts
| Role | Username | Password | Dashboard URL |
|------|----------|----------|---------------|
| Technician | technician1 | password123 | `/dashboard/technician` |
| Engineer | engineer1 | password123 | `/dashboard/engineer` |
| Deputy Manager | dm1 | password123 | `/dashboard/dm` |
| Deputy General Manager | dgm1 | password123 | `/dashboard/dgm` |

---

## 🔧 TECHNICIAN WORKFLOW

### Dashboard Overview
**URL**: `/dashboard/technician`

**What you'll see:**
- Statistics cards (Equipment count, Your monitoring records, Notifications)
- Equipment list table
- Recent monitoring records
- Navigation sidebar

### Step-by-Step Tasks

#### 1. Daily Monitoring (UC-01)
**Purpose**: Record daily equipment readings

**Steps:**
1. Click **"Forms"** → **"Daily Monitoring"** (or go to `/forms/daily-monitoring`)
2. Select **Equipment** from dropdown
3. Enter **Monitoring Date**
4. Select **Shift** (Morning/Afternoon/Night)
5. Enter readings:
   - **Voltage (V)**: e.g., 230
   - **Current (A)**: e.g., 50
   - **Power Factor**: e.g., 0.95
6. Select **Operational Status** (Normal/Warning/Critical)
7. Add **Observations** (optional notes)
8. Click **"Submit Monitoring Data"**
9. Success message appears, data is saved

**Result**: Equipment status automatically updates if readings are critical

#### 2. Equipment Status View
**Purpose**: View all equipment information

**Steps:**
1. Click **"Forms"** → **"Equipment Status"** (or go to `/forms/equipment-status`)
2. View table showing:
   - Equipment Code & Name
   - Type & Location
   - Current Status
   - Maintenance dates
3. Use this to decide which equipment to monitor

#### 3. Report a Fault
**Purpose**: Report equipment issues

**Steps:**
1. From dashboard, click **"Report Fault"** button (or use fault reporting feature)
2. Select **Equipment** with the fault
3. Enter **Fault Description** (detailed description)
4. Select **Severity** (Low/Medium/High/Critical)
5. Click **"Submit"**
6. Fault is created and Engineers are notified

**Result**: Fault appears in Engineer dashboard for investigation

#### 4. Data Re-verification (UC-05)
**Purpose**: Re-verify previously recorded data

**Steps:**
1. Click **"Forms"** → **"Data Re-verification"** (or go to `/forms/data-reverification`)
2. Enter **Original Monitoring Record ID** (or select from monitoring history)
3. Enter **New Readings**:
   - New Voltage
   - New Current
   - New Power Factor
4. (Optional) Enter custom **Tolerance Levels**
5. Click **"Submit Re-verification"**
6. System compares old vs new readings
7. View comparison results
8. If discrepancies found, Engineer approval is required

#### 5. Performance Report Generation (UC-04)
**Purpose**: Create performance reports from monitoring data

**Steps:**
1. Click **"Forms"** → **"Performance Report"** (or go to `/forms/performance-report`)
2. **Step 1**: Select Report Period
   - Choose Report Type (Weekly/Monthly/Custom)
   - Enter Period Start and End dates
   - Click **"Compile Data"**
3. **Step 2**: Review Compiled Data Summary
   - View statistics (averages, counts, etc.)
4. **Step 3**: Create Report
   - Enter **Analysis** (interpretation of data)
   - Enter **Recommendations**
   - Click **"Save as Draft"** or **"Submit for Approval"**
5. Report goes to DM for approval

#### 6. View Monitoring History
**Purpose**: View your past monitoring records

**Steps:**
1. Click **"Views"** → **"Monitoring History"** (or go to `/views/monitoring-history`)
2. See all your monitoring records
3. Filter and search as needed

### Technician Dashboard Features
- **Quick Stats**: Equipment count, your records count, notifications
- **Equipment Table**: All equipment with status
- **Recent Monitoring**: Last 10 entries you created
- **Notifications**: Unread notifications count (click bell icon)

---

## 👨‍💻 ENGINEER WORKFLOW

### Dashboard Overview
**URL**: `/dashboard/engineer`

**What you'll see:**
- Statistics (Faults, Unresolved faults, Notifications)
- Pending faults table
- Critical monitoring alerts
- Navigation sidebar

### Step-by-Step Tasks

#### 1. View and Investigate Faults
**Purpose**: Investigate reported faults

**Steps:**
1. From dashboard, view **"Pending Faults"** table
2. Click on a fault to view details
3. Review:
   - Equipment information
   - Fault description
   - Severity level
   - Reporter information

#### 2. Root Cause Analysis (UC-06)
**Purpose**: Analyze faults and identify root causes

**Steps:**
1. Click **"Forms"** → **"Root Cause Analysis"** (or go to `/forms/root-cause-analysis`)
2. Select **Fault ID** (or it may be pre-filled if accessed from fault)
3. Enter **Root Cause** (main cause of the fault)
4. Enter **Contributing Factors** (factors that contributed)
5. Click **"Submit RCA"**
6. RCA is linked to the fault

**Result**: Fault status may update, ready for resolution report

#### 3. Technical Reference (UC-07)
**Purpose**: Document technical drawings, manuals, specifications

**Steps:**
1. Click **"Forms"** → **"Technical Reference"** (or go to `/forms/technical-reference`)
2. Select **Equipment**
3. Select **Reference Type** (Drawing/Manual/History/Specification)
4. Enter **Document Name**
5. Enter **Document Version** (optional)
6. Enter **Findings** (what you found)
7. Enter **Relevance** (how it relates)
8. Enter **Conclusions** (your conclusions)
9. Click **"Submit Reference"**

#### 4. Documentation Package (UC-09, UC-10)
**Purpose**: Create complete documentation packages for fault resolution

**Steps:**
1. Click **"Forms"** → **"Documentation Package"** (or go to `/forms/documentation-package`)
2. Enter **Fault ID** (if not pre-filled)
3. Enter **Package Name** (e.g., "Fault Resolution Documentation - Equipment #123")
4. Select **Documentation Type** (optional)
5. Click **"Create Package"**
6. **Add Documents**:
   - Enter **Document Name**
   - Select **Document Type** (Report/Drawing/Manual/Certificate/Other)
   - Enter **Version** (optional)
   - Enter **Content/Description**
   - Click **"Add Document"**
   - Repeat for all documents needed
7. **Complete Package**:
   - Ensure all items are marked as "completed"
   - Click **"Mark Package Complete"**
8. **Submit for Approval**:
   - Click **"Submit for Approval"**
   - Package goes to DM/DGM for approval

#### 5. Draft Resolution Report (UC-08)
**Purpose**: Create resolution reports for faults

**Steps:**
1. Click **"Forms"** → **"Draft Resolution"** (or go to `/forms/draft-resolution`)
2. Select **Fault ID** (may be pre-filled)
3. Enter **Resolution Description** (how the fault was resolved)
4. Enter **Actions Taken** (detailed actions)
5. Enter **Preventive Measures** (optional - how to prevent recurrence)
6. Click **"Save as Draft"** or **"Submit for Approval"**
7. If submitted, report goes to DM for approval

#### 6. Delivery/Service Verification (UC-13, UC-14)
**Purpose**: Verify vendor deliveries and services

**Steps:**
1. Click **"Forms"** → **"Delivery Verification"** (or go to `/forms/delivery-verification`)
2. Select **Verification Type** (Delivery or Service)
3. Select **Vendor** from dropdown
4. Select **Equipment**
5. Enter date:
   - If Delivery: Enter **Delivery Date**
   - If Service: Enter **Service Date**
6. Enter **Quality Assessment** (optional notes)
7. Enter **Supporting Documents** (reference numbers, file locations)
8. Click **"Create Verification"**
9. Verification goes to DGM for final verification

#### 7. Vendor Management (UC-15)
**Purpose**: Manage vendor information

**Steps:**
1. Click **"Forms"** → **"Vendor Management"** (or go to `/forms/vendor-management`)
2. **Create New Vendor**:
   - Enter **Vendor Name**
   - Enter **Vendor Code** (unique identifier)
   - Enter **Contact Information**
   - Enter **Material List** (materials/services provided)
   - Click **"Create Vendor"**
3. **Edit Existing Vendor**:
   - Click **"Edit"** button next to vendor in the table
   - Modify information
   - Toggle **Active Vendor** checkbox
   - Click **"Update Vendor"**
4. **Activate/Deactivate**:
   - Click **"Activate"** or **"Deactivate"** buttons

### Engineer Dashboard Features
- **Pending Faults**: All faults awaiting investigation
- **Critical Monitoring**: Equipment with critical readings
- **Notifications**: System notifications
- **Quick Actions**: Access to all forms

---

## 👔 DM (DEPUTY MANAGER) WORKFLOW

### Dashboard Overview
**URL**: `/dashboard/dm`

**What you'll see:**
- Statistics (Pending approvals, Total faults, Unresolved faults, Notifications)
- Pending reports table
- Recent faults overview

### Step-by-Step Tasks

#### 1. Review and Approve Performance Reports (UC-04)
**Purpose**: Approve technician performance reports

**Steps:**
1. From dashboard, view **"Pending Reports"** table
2. Click on a report to view details
3. Review:
   - Report period
   - Compiled data and statistics
   - Analysis provided
   - Recommendations
4. **Approve or Reject**:
   - Click **"Approve"** to approve the report
   - Or click **"Reject"** if changes needed
5. Report status updates

#### 2. Review and Approve Resolution Reports (UC-11)
**Purpose**: Approve engineer resolution reports

**Steps:**
1. Go to **"Views"** → **"Report Review"** (or `/views/report-review`)
2. View pending resolution reports
3. Review:
   - Fault details
   - Root cause analysis
   - Resolution description
   - Actions taken
   - Preventive measures
4. **Approve**:
   - If approved, fault is automatically marked as resolved
   - Equipment status updates to operational
5. **Reject** (if needed):
   - Add rejection reason
   - Report goes back to engineer for revision

#### 3. Review and Approve Documentation Packages (UC-10)
**Purpose**: Approve documentation packages

**Steps:**
1. Access pending documentation packages (via API or view)
2. Review package contents:
   - Package information
   - All documentation items
   - Completeness
3. **Approve** or **Reject** the package

#### 4. Historical Data Analysis
**Purpose**: Analyze historical monitoring data

**Steps:**
1. Go to **"Views"** → **"Historical Data"** (or `/views/historical-data`)
2. Select equipment or date range
3. View trends and patterns
4. Analyze data for decision-making

#### 5. Trend Comparison
**Purpose**: Compare data across time periods

**Steps:**
1. Go to **"Views"** → **"Trend Comparison"** (or `/views/trend-comparison`)
2. Select comparison parameters
3. View comparative analysis
4. Identify improvements or issues

#### 6. Escalation Review (UC-12)
**Purpose**: Review escalated faults

**Steps:**
1. View escalations in dashboard
2. Review escalation reasons
3. Make management decisions
4. Resolve or escalate further to DGM

### DM Dashboard Features
- **Pending Approvals**: All reports needing approval
- **Fault Overview**: System-wide fault status
- **Analytics**: Historical data and trends

---

## 👑 DGM (DEPUTY GENERAL MANAGER) WORKFLOW

### Dashboard Overview
**URL**: `/dashboard/dgm`

**What you'll see:**
- Statistics (Pending approvals, Total faults, Unresolved faults, Notifications)
- Pending reports table
- Complete faults overview

### Step-by-Step Tasks

#### 1. All DM Functions
DGM can perform all DM functions (see DM workflow above)

#### 2. Verify Delivery/Service (UC-13, UC-14)
**Purpose**: Final verification of vendor deliveries and services

**Steps:**
1. Access pending verifications (via system or notifications)
2. Review verification details:
   - Vendor information
   - Equipment information
   - Quality assessment
   - Supporting documents
3. **Verify**:
   - Select **Verification Status** (Verified/Rejected)
   - Set **Compliance Status** (Compliant/Non-Compliant/Requires Action)
   - Click **"Verify"**
4. Verification is finalized

#### 3. Approved Reports Archive
**Purpose**: View all approved reports

**Steps:**
1. Go to **"Reports"** → **"Approved Reports"** (or `/reports/approved-reports`)
2. View complete archive of approved reports
3. Filter and search reports
4. Access report details

#### 4. System-Wide Oversight
**Purpose**: Monitor entire system

**Steps:**
1. View all dashboards and reports
2. Monitor all equipment status
3. Review all faults and resolutions
4. Analyze system-wide performance
5. Make strategic decisions

### DGM Dashboard Features
- **Complete System View**: All data and reports
- **Strategic Analytics**: High-level insights
- **Final Authority**: Ultimate approval authority

---

## 🔄 COMPLETE WORKFLOW EXAMPLES

### Example 1: Fault Resolution Workflow (End-to-End)

```
1. TECHNICIAN
   ├─ Monitors equipment daily
   ├─ Detects abnormal reading → Reports Fault
   └─ Fault severity: High
      ↓
2. ENGINEER
   ├─ Receives notification about fault
   ├─ Views fault details
   ├─ Performs Root Cause Analysis (RCA)
   ├─ Creates Documentation Package
   │  ├─ Adds multiple documents
   │  └─ Submits package for approval
   ├─ Creates Draft Resolution Report
   │  ├─ Describes resolution
   │  ├─ Documents actions taken
   │  └─ Submits for approval
   └─ Creates Technical Reference (optional)
      ↓
3. DM
   ├─ Reviews Documentation Package → Approves
   ├─ Reviews Resolution Report
   ├─ Approves Report
   └─ Fault automatically marked as RESOLVED
      ↓
4. SYSTEM
   ├─ Equipment status → Operational
   └─ Notifications sent to relevant users
```

### Example 2: Vendor Delivery Verification Workflow

```
1. ENGINEER
   ├─ Creates Delivery Verification
   ├─ Selects Vendor & Equipment
   ├─ Enters delivery date
   ├─ Adds quality assessment
   └─ Submits for verification
      ↓
2. DGM
   ├─ Reviews verification
   ├─ Checks supporting documents
   ├─ Verifies delivery
   └─ Sets compliance status
      ↓
3. SYSTEM
   └─ Verification finalized and recorded
```

### Example 3: Performance Report Workflow

```
1. TECHNICIAN
   ├─ Creates Performance Report
   ├─ Selects report period (e.g., Weekly)
   ├─ Compiles monitoring data
   ├─ Provides analysis
   ├─ Provides recommendations
   └─ Submits for approval
      ↓
2. DM
   ├─ Reviews performance report
   ├─ Checks data compilation
   ├─ Reviews analysis & recommendations
   └─ Approves Report
      ↓
3. SYSTEM
   └─ Report archived and available for DGM
```

---

## 📱 Navigation Guide

### Sidebar Menu Structure

#### Technician Sidebar
- Dashboard
- Forms
  - Daily Monitoring
  - Equipment Status
  - Data Re-verification
  - Performance Report
- Views
  - Monitoring History

#### Engineer Sidebar
- Dashboard
- Forms
  - Root Cause Analysis
  - Draft Resolution
  - Documentation Package
  - Technical Reference
  - Delivery Verification
  - Vendor Management
- Views
  - Fault List
  - Escalation Timeline

#### DM Sidebar
- Dashboard
- Views
  - Report Review
  - Historical Data
  - Trend Comparison
  - Escalation Timeline
- Reports
  - (Access to various reports)

#### DGM Sidebar
- Dashboard
- Views
  - Report Review
  - Historical Data
  - Trend Comparison
  - Escalation Timeline
- Reports
  - Approved Reports Archive

---

## 🔔 Notifications System

### Notification Types
- **Info**: General information
- **Warning**: Warnings about equipment or data
- **Error**: Critical errors
- **Success**: Successful operations
- **Escalation**: Escalation notifications

### Viewing Notifications
1. Click the **bell icon** (🔔) in the top navigation bar
2. View unread notifications
3. Click **"Mark all read"** to mark all as read
4. Click on individual notifications to view details

---

## 💡 Tips and Best Practices

1. **Always Log Out**: Click "Logout" when done to protect your session
2. **Check Notifications**: Regularly check notifications for important updates
3. **Complete Forms Fully**: Fill all required fields for accurate data
4. **Save Drafts**: Use "Save as Draft" for work in progress
5. **Review Before Submit**: Review all information before submitting for approval
6. **Use Equipment Codes**: Use equipment codes for easy reference
7. **Document Everything**: Provide detailed descriptions and observations

---

## 🆘 Troubleshooting

### Cannot Login
- Verify username and password are correct
- Check if user exists in database
- Run `python setup_db.py` to create test users

### Database Not Found
- Run `python app.py` once to create the database
- Database file: `operations_monitoring.db` in project root

### Port Already in Use
- Change port in `app.py` (line 9): `app.run(debug=True, host='0.0.0.0', port=5001)`
- Or stop other applications using port 5000

### Forms Not Loading
- Check browser console for errors
- Verify you're logged in with correct role
- Clear browser cache and try again

---

## 📚 Additional Resources

- **Database Schema**: See `app/database/db_connection.py`
- **Architecture**: See `ARCHITECTURE.md`
- **Roles Details**: See `ROLES_AND_FUNCTIONALITIES.md`
- **Implementation Status**: See `IMPLEMENTATION_STATUS.md`

---

## ✅ Quick Reference Checklist

### First Time Setup
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Setup database: `python setup_db.py`
- [ ] Start application: `python app.py`
- [ ] Access: `http://localhost:5000`
- [ ] Login with test account

### Daily Work (Technician)
- [ ] Login as technician1
- [ ] View equipment status
- [ ] Enter daily monitoring data
- [ ] Report any faults
- [ ] Check notifications
- [ ] Logout

### Daily Work (Engineer)
- [ ] Login as engineer1
- [ ] Review pending faults
- [ ] Perform RCA for faults
- [ ] Create resolution reports
- [ ] Manage documentation packages
- [ ] Check notifications
- [ ] Logout

### Daily Work (DM/DGM)
- [ ] Login as dm1 or dgm1
- [ ] Review pending reports
- [ ] Approve/reject reports
- [ ] Review historical data
- [ ] Check notifications
- [ ] Logout

---

**End of Guide** - For technical support, refer to the codebase documentation or contact the development team.




