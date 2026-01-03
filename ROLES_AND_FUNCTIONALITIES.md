# Roles and Functionalities Guide

## Role Hierarchy

The system implements a **4-tier role hierarchy** with increasing permissions:

```
Technician (Level 1) 
    ↓
Engineer (Level 2)
    ↓
Deputy Manager - DM (Level 3)
    ↓
Deputy General Manager - DGM (Level 4)
```

**Higher roles inherit permissions from lower roles** - meaning a DGM can do everything a DM, Engineer, and Technician can do.

---

## 🔧 1. TECHNICIAN ROLE

### **Role Level**: 1 (Entry Level)
### **Dashboard**: `/dashboard/technician`

### **Primary Responsibilities:**
- **Data Collection**: Daily monitoring of equipment
- **Issue Reporting**: Report faults when detected
- **Equipment Status**: View equipment status and information

### **Functionalities:**

#### ✅ **Daily Monitoring**
- **Access**: `Forms → Daily Monitoring`
- **What they can do:**
  - Enter daily monitoring data for equipment
  - Record temperature readings (°C)
  - Record pressure readings (PSI)
  - Record vibration levels
  - Set operational status (Normal/Warning/Critical)
  - Add observations and notes
  - Select equipment from available list
  - View monitoring date

- **Impact**: 
  - Monitoring data triggers automatic status updates
  - Critical readings automatically mark equipment as "faulty"
  - Data feeds into historical analysis

#### ✅ **Equipment Status Viewing**
- **Access**: `Forms → Equipment Status`
- **What they can see:**
  - All equipment in the system
  - Equipment codes and names
  - Equipment types and locations
  - Current status (Operational/Maintenance/Faulty/Decommissioned)
  - Last maintenance date
  - Next maintenance date

#### ✅ **Fault Reporting**
- **What they can do:**
  - Report faults when equipment issues are detected
  - Select equipment with fault
  - Describe fault in detail
  - Set fault severity (Low/Medium/High/Critical)
  - Fault automatically creates notification for Engineers

#### ✅ **Monitoring History**
- **Access**: `Views → Monitoring History`
- **What they can see:**
  - Their own monitoring records
  - Historical data they've entered
  - Temperature, pressure, vibration trends
  - Status history over time

#### ✅ **Dashboard Features:**
- **Statistics Cards:**
  - Total Equipment count
  - Personal monitoring records count
  - Unread notifications count

- **Equipment Table:**
  - View all available equipment
  - See equipment status at a glance
  - Quick access to monitoring form for each equipment

- **Recent Monitoring Records:**
  - Last 10 monitoring entries
  - Quick status overview

### **What Technicians CANNOT Do:**
- ❌ Cannot perform Root Cause Analysis
- ❌ Cannot create resolution reports
- ❌ Cannot approve reports
- ❌ Cannot view escalation timelines
- ❌ Cannot access historical data analysis
- ❌ Cannot view all faults (only their own reports)

### **Notifications Received:**
- Equipment status changes
- Fault acknowledgment
- Critical monitoring alerts

---

## 🔬 2. ENGINEER ROLE

### **Role Level**: 2 (Technical Analysis)
### **Dashboard**: `/dashboard/engineer`

### **Primary Responsibilities:**
- **Fault Analysis**: Investigate and analyze reported faults
- **Root Cause Analysis**: Determine root causes of faults
- **Resolution Planning**: Create resolution reports
- **Technical Oversight**: Monitor critical equipment status

### **Functionalities:**

#### ✅ **Root Cause Analysis (RCA)**
- **Access**: `Forms → Root Cause Analysis`
- **What they can do:**
  - Analyze reported faults
  - Identify root causes
  - Document contributing factors
  - Link RCA to specific faults
  - Create detailed analysis reports

- **Impact**: 
  - RCA data feeds into resolution reports
  - Helps in preventive measures planning
  - Supports decision-making for managers

#### ✅ **Draft Resolution Reports**
- **Access**: `Forms → Draft Resolution`
- **What they can do:**
  - Create draft resolution reports
  - Describe resolution actions taken
  - Document preventive measures
  - Link to fault and RCA
  - Save as draft for later editing
  - Submit for manager approval

- **Workflow:**
  1. Create draft report
  2. Fill in resolution details
  3. Save as draft (can edit later)
  4. Submit for approval (sends to DM/DGM)

#### ✅ **Fault Investigation**
- **Access**: `Views → Fault List`
- **What they can see:**
  - All faults in the system
  - Filter by status (Reported/Investigating/Resolved/Escalated)
  - Fault details and descriptions
  - Severity levels
  - Equipment associations
  - Reported dates

- **What they can do:**
  - View all fault information
  - Update fault status to "Investigating"
  - Access fault details for RCA
  - Track fault resolution progress

#### ✅ **Escalation Timeline**
- **Access**: `Views → Escalation Timeline`
- **What they can see:**
  - Escalation history
  - Multi-level escalation paths
  - Escalation reasons
  - Timeline of escalations

#### ✅ **Critical Monitoring Alerts**
- **What they can see:**
  - All critical monitoring records
  - Equipment with critical status
  - Temperature/pressure/vibration alerts
  - Real-time critical alerts

#### ✅ **Dashboard Features:**
- **Statistics Cards:**
  - Total faults count
  - Unresolved faults count
  - Critical monitoring alerts count
  - Unread notifications count

- **Recent Faults Table:**
  - Last 10 reported faults
  - Quick access to analyze faults
  - Status and severity indicators

- **Critical Monitoring Alerts:**
  - Real-time critical status alerts
  - Equipment requiring immediate attention

### **What Engineers CANNOT Do:**
- ❌ Cannot approve resolution reports
- ❌ Cannot access historical data analysis (DM/DGM only)
- ❌ Cannot view trend comparisons
- ❌ Cannot access approved reports archive
- ❌ Cannot perform system-wide oversight

### **Notifications Received:**
- New fault reports (especially high/critical severity)
- Escalation notifications
- Critical monitoring alerts
- Report approval status updates

---

## 👔 3. DEPUTY MANAGER (DM) ROLE

### **Role Level**: 3 (Management & Approval)
### **Dashboard**: `/dashboard/dm`

### **Primary Responsibilities:**
- **Report Approval**: Review and approve resolution reports
- **Decision Making**: Make approval/rejection decisions
- **Data Analysis**: Analyze historical data and trends
- **Oversight**: Monitor system-wide operations

### **Functionalities:**

#### ✅ **Report Review & Approval**
- **Access**: `Views → Report Review`
- **What they can do:**
  - View all pending resolution reports
  - Review resolution descriptions
  - Review actions taken
  - Review preventive measures
  - **Approve reports** (approves resolution)
  - **Reject reports** (sends back for revision)
  - View report details and history

- **Impact**: 
  - Approval automatically marks fault as "resolved"
  - Updates equipment status to "operational"
  - Triggers notifications to report preparer
  - Creates audit log entry

#### ✅ **Historical Data Analysis**
- **Access**: `Views → Historical Data`
- **What they can see:**
  - Historical monitoring data
  - Equipment performance trends
  - Fault history patterns
  - Resolution effectiveness metrics
  - Time-based analysis

#### ✅ **Trend Comparison**
- **Access**: `Views → Trend Comparison`
- **What they can do:**
  - Compare equipment performance over time
  - Compare different equipment
  - Analyze trends and patterns
  - Identify recurring issues
  - Performance benchmarking

#### ✅ **Fault Oversight**
- **What they can see:**
  - All faults in the system
  - Fault status and progress
  - Escalation status
  - Resolution status

#### ✅ **Dashboard Features:**
- **Statistics Cards:**
  - Pending approvals count
  - Total faults count
  - Unresolved faults count
  - Unread notifications count

- **Pending Reports Table:**
  - All reports awaiting approval
  - Report details and preparer info
  - Quick access to review

- **Recent Faults Overview:**
  - System-wide fault status
  - Fault distribution

### **What DMs CANNOT Do:**
- ❌ Cannot access approved reports archive (DGM only)
- ❌ Cannot perform system-wide administrative functions
- ❌ Cannot modify user roles (if implemented)

### **Notifications Received:**
- Reports pending approval
- Escalated faults
- Critical system alerts
- High-priority notifications

---

## 👑 4. DEPUTY GENERAL MANAGER (DGM) ROLE

### **Role Level**: 4 (Executive Oversight)
### **Dashboard**: `/dashboard/dgm`

### **Primary Responsibilities:**
- **Executive Oversight**: System-wide monitoring and control
- **Final Approval**: Ultimate authority for report approvals
- **Archive Management**: Access to approved reports archive
- **Strategic Analysis**: High-level data analysis and reporting

### **Functionalities:**

#### ✅ **All DM Functionalities**
- Everything a DM can do, plus:

#### ✅ **Report Review & Approval (Enhanced)**
- **Access**: `Views → Report Review`
- **What they can do:**
  - All DM approval capabilities
  - Final approval authority
  - Override decisions if needed
  - View all reports (pending and approved)

#### ✅ **Approved Reports Archive**
- **Access**: `Reports → Approved Reports`
- **What they can see:**
  - Complete archive of approved reports
  - Historical resolution reports
  - Download/print reports
  - Report analytics
  - Resolution effectiveness data

#### ✅ **System-Wide Oversight**
- **What they can see:**
  - All equipment status
  - All faults (resolved and unresolved)
  - All monitoring data
  - All escalations
  - Complete system statistics

#### ✅ **Enhanced Analytics**
- **What they can access:**
  - Comprehensive historical data
  - Advanced trend analysis
  - System performance metrics
  - Operational efficiency reports
  - Strategic insights

#### ✅ **Dashboard Features:**
- **Statistics Cards:**
  - Pending approvals count
  - Total faults count
  - Unresolved faults count
  - Unread notifications count

- **Pending Reports Table:**
  - All reports awaiting approval
  - Priority indicators
  - Quick approval actions

- **Complete Faults Overview:**
  - All faults in the system
  - Complete status tracking
  - System-wide view

### **What DGMs CAN Do (Exclusive):**
- ✅ Access approved reports archive
- ✅ System-wide administrative oversight
- ✅ Complete system analytics
- ✅ Strategic reporting capabilities
- ✅ Final decision authority

### **Notifications Received:**
- All high-priority notifications
- Critical escalations
- Reports pending approval
- System-wide alerts
- Strategic alerts

---

## 🔄 Workflow Between Roles

### **Typical Workflow:**

```
1. TECHNICIAN
   ↓ (Reports fault)
   
2. ENGINEER
   ↓ (Performs RCA)
   ↓ (Creates resolution report)
   ↓ (Submits for approval)
   
3. DM or DGM
   ↓ (Reviews report)
   ↓ (Approves/Rejects)
   ↓ (If approved: Fault marked resolved)
```

### **Escalation Workflow:**

```
Technician → Engineer → DM → DGM
(Each level can escalate to next)
```

---

## 📊 Permission Matrix

| Functionality | Technician | Engineer | DM | DGM |
|--------------|------------|----------|----|----|
| Daily Monitoring | ✅ | ❌ | ❌ | ❌ |
| Equipment Status View | ✅ | ✅ | ✅ | ✅ |
| Fault Reporting | ✅ | ✅ | ✅ | ✅ |
| Root Cause Analysis | ❌ | ✅ | ✅ | ✅ |
| Draft Resolution Reports | ❌ | ✅ | ✅ | ✅ |
| Report Approval | ❌ | ❌ | ✅ | ✅ |
| Historical Data Analysis | ❌ | ❌ | ✅ | ✅ |
| Trend Comparison | ❌ | ❌ | ✅ | ✅ |
| Approved Reports Archive | ❌ | ❌ | ❌ | ✅ |
| System-Wide Oversight | ❌ | ❌ | ❌ | ✅ |

---

## 🔔 Notification System by Role

### **Technician Notifications:**
- Equipment status changes
- Fault acknowledgment
- Critical alerts for their equipment

### **Engineer Notifications:**
- New fault reports (especially critical)
- Escalation notifications
- Critical monitoring alerts
- Report approval status

### **DM Notifications:**
- Reports pending approval
- Escalated faults
- Critical system alerts
- High-priority issues

### **DGM Notifications:**
- All high-priority notifications
- Critical escalations
- Strategic alerts
- System-wide issues

---

## 🎯 Key Features by Role

### **Technician Key Features:**
1. ✅ Simple, focused interface
2. ✅ Quick monitoring data entry
3. ✅ Easy fault reporting
4. ✅ Personal monitoring history

### **Engineer Key Features:**
1. ✅ Technical analysis tools
2. ✅ RCA documentation
3. ✅ Resolution report creation
4. ✅ Fault investigation tools

### **DM Key Features:**
1. ✅ Approval workflow
2. ✅ Data analysis tools
3. ✅ Trend comparison
4. ✅ Management oversight

### **DGM Key Features:**
1. ✅ Executive dashboard
2. ✅ Complete system access
3. ✅ Archive management
4. ✅ Strategic analytics

---

## 🔐 Security & Access Control

- **Role-Based Redirect**: Users automatically redirected to their role dashboard
- **Permission Checking**: Each route checks user role before access
- **Hierarchical Permissions**: Higher roles can access lower role features
- **Session Management**: Role stored in session, validated on each request
- **Audit Logging**: All actions logged with user role information

---

## 📝 Summary

**Technician** = Data Entry & Reporting
**Engineer** = Analysis & Resolution Planning  
**DM** = Approval & Data Analysis
**DGM** = Executive Oversight & Archive

Each role is designed for specific responsibilities in the operations and monitoring workflow, with clear boundaries and escalation paths.




