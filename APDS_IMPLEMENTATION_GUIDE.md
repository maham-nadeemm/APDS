# APDS Implementation Guide

This guide provides the exact pattern for updating all remaining forms and views with DMO/DNO functionality, proper controls, labels, feedback, and support.

## ✅ Completed Updates

1. ✅ `app/templates/base.html` - Changed app name to "APDS"
2. ✅ `app/templates/auth/login.html` - Changed app name to "APDS"
3. ✅ `app/static/js/dmo_dno.js` - Created DMO/DNO utilities
4. ✅ `app/templates/forms/daily_monitoring.html` - Full DMO/DNO implementation
5. ✅ `app/templates/forms/report_fault.html` - Full DMO/DNO implementation
6. ✅ `app/templates/forms/vendor_management.html` - Full DMO/DNO implementation
7. ✅ `app/templates/views/monitoring_history.html` - Full DMO/DNO implementation

## 📋 Remaining Forms to Update (8 forms)

### Pattern for Form Updates

Each form needs:

1. **Title Update**: Change title to include "- APDS"
2. **DMO Panel**: Add DMO operations panel (Add, Edit, Delete, Save, Cancel, Search, Help, Refresh, Load Defaults)
3. **DNO Panel**: Add DNO navigation panel (First, Previous, Next, Last, Record Info)
4. **Form Updates**:
   - Add hidden ID field: `<input type="hidden" id="[entity]_id" name="[entity]_id">`
   - Add `name="mainForm"` to form tag
   - Add proper labels with `title` attributes
   - Add `<small>` help text for each field
   - Add validation messages
5. **Feedback Panel**: Add feedback display area
6. **JavaScript**: Initialize DMO/DNO with proper configuration

### Forms to Update:

1. `app/templates/forms/equipment_status.html` - Table view, needs DMO/DNO panels
2. `app/templates/forms/root_cause_analysis.html` - Form with DMO/DNO
3. `app/templates/forms/draft_resolution.html` - Form with DMO/DNO
4. `app/templates/forms/performance_report.html` - Form with DMO/DNO
5. `app/templates/forms/data_reverification.html` - Form with DMO/DNO
6. `app/templates/forms/technical_reference.html` - Form with DMO/DNO
7. `app/templates/forms/documentation_package.html` - Form with DMO/DNO
8. `app/templates/forms/delivery_verification.html` - Form with DMO/DNO

## 📋 Remaining Views to Update (5 views)

### Pattern for View Updates

Each view needs:

1. **Title Update**: Change title to include "- APDS"
2. **DMO Panel**: Add DMO operations panel (Add, Edit, Delete, Search, Help, Refresh)
3. **DNO Panel**: Add DNO navigation panel (First, Previous, Next, Last, Record Info)
4. **Feedback Panel**: Add feedback display area
5. **JavaScript**: 
   - Track records array and current index
   - Implement search functionality
   - Implement navigation between records
   - Add row selection highlighting

### Views to Update:

1. `app/templates/views/fault_list.html` - Table view with DMO/DNO
2. `app/templates/views/escalation_timeline.html` - Timeline view with DMO/DNO
3. `app/templates/views/historical_data.html` - Data view with DMO/DNO
4. `app/templates/views/trend_comparison.html` - Comparison view with DMO/DNO
5. `app/templates/views/report_review.html` - Review view with DMO/DNO

## 📋 Dashboards to Update (4 dashboards)

### Pattern for Dashboard Updates

Each dashboard needs:

1. **Title Update**: Change any references from "Operations & Monitoring System" or "O&M System" to "APDS"
2. **Branding**: Update sidebar headers and titles

### Dashboards to Update:

1. `app/templates/dashboards/technician.html`
2. `app/templates/dashboards/engineer.html`
3. `app/templates/dashboards/dm.html`
4. `app/templates/dashboards/dgm.html`

## 🔧 Standard DMO Panel HTML

```html
<!-- DMO Operations Panel -->
<div class="dmo-panel" style="padding: 1rem 1.5rem; background-color: #0f0f1a; border-bottom: 1px solid var(--card-border);">
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center;">
        <button type="button" id="btnAdd" class="btn btn-sm btn-primary" title="Add new record">Add</button>
        <button type="button" id="btnEdit" class="btn btn-sm btn-primary" title="Edit selected record">Edit</button>
        <button type="button" id="btnDelete" class="btn btn-sm btn-danger" title="Delete selected record">Delete</button>
        <button type="button" id="btnSave" class="btn btn-sm btn-success" title="Save current record">Save</button>
        <button type="button" id="btnCancel" class="btn btn-sm btn-secondary" title="Cancel current operation">Cancel</button>
        <div style="flex: 1; min-width: 200px;">
            <input type="text" id="searchInput" class="form-input" placeholder="Search records..." style="width: 100%;">
        </div>
        <button type="button" id="btnSearch" class="btn btn-sm btn-info" title="Search records">Search</button>
        <button type="button" id="btnRefresh" class="btn btn-sm btn-secondary" title="Refresh data">Refresh</button>
        <button type="button" id="btnLoadDefaults" class="btn btn-sm btn-secondary" title="Load default values">Load Defaults</button>
        <button type="button" id="btnHelp" class="btn btn-sm btn-info" title="Show help">Help</button>
    </div>
</div>
```

## 🔧 Standard DNO Panel HTML

```html
<!-- DNO Navigation Panel -->
<div class="dno-panel" style="padding: 0.75rem 1.5rem; background-color: #0a0a15; border-bottom: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center;">
    <div style="display: flex; gap: 0.5rem;">
        <button type="button" id="btnFirst" class="btn btn-sm btn-secondary" title="Go to first record">⏮ First</button>
        <button type="button" id="btnPrevious" class="btn btn-sm btn-secondary" title="Go to previous record">⏪ Previous</button>
        <button type="button" id="btnNext" class="btn btn-sm btn-secondary" title="Go to next record">Next ⏩</button>
        <button type="button" id="btnLast" class="btn btn-sm btn-secondary" title="Go to last record">Last ⏭</button>
    </div>
    <div id="recordInfo" style="color: var(--text-secondary); font-size: 0.9rem;">No records</div>
</div>
```

## 🔧 Standard Feedback Panel HTML

```html
<!-- Feedback Panel -->
<div id="feedbackPanel" style="margin-top: 1rem; padding: 0.75rem; background-color: #0a0a15; border-radius: 6px; display: none;">
    <div id="feedbackMessage" style="color: var(--text-primary);"></div>
</div>
```

## 🔧 Standard JavaScript Initialization Pattern

```javascript
let records = [];
let currentRecordIndex = -1;

document.addEventListener('DOMContentLoaded', function() {
    const { dmo, dno, support } = initializeDMO_DNO({
        dmo: {
            formId: '[FORM_ID]',
            apiEndpoint: '/api/[ENDPOINT]',
            onSave: function(data) {
                loadRecords();
            },
            onDelete: function(id) {
                loadRecords();
            },
            onSearch: function(query) {
                searchRecords(query);
            },
            onRefresh: function() {
                loadRecords();
            },
            onLoadDefaults: function() {
                // Set default values
            },
            onHelp: function() {
                alert('[Form-specific help message]');
            }
        },
        dno: {
            records: records,
            onRecordChange: function(record, index) {
                populateForm(record);
                currentRecordIndex = index;
            }
        }
    });
    
    // Add tooltips to controls
    support.addTooltip('field_id', 'Tooltip message');
    
    loadRecords();
});

async function loadRecords() {
    try {
        const response = await fetch('/api/[ENDPOINT]?limit=1000');
        const result = await response.json();
        if (result.success) {
            records = result.data || [];
            if (window.dno) {
                window.dno.setRecords(records);
            }
            showFeedback(`Loaded ${records.length} records`, 'success');
        }
    } catch (error) {
        console.error('Error loading records:', error);
    }
}

function populateForm(record) {
    if (!record) return;
    // Populate form fields with record data
    if (window.dmo) {
        window.dmo.currentRecordId = record.id;
        window.dmo.isEditMode = true;
        window.dmo.updateButtonStates();
    }
}

function searchRecords(query) {
    if (!query) {
        loadRecords();
        return;
    }
    const filtered = records.filter(r => {
        const searchStr = query.toLowerCase();
        // Add search logic
    });
    if (window.dno) {
        window.dno.setRecords(filtered);
    }
    showFeedback(`Found ${filtered.length} matching records`, 'info');
}

function showFeedback(message, type = 'info') {
    const panel = document.getElementById('feedbackPanel');
    const msg = document.getElementById('feedbackMessage');
    if (panel && msg) {
        panel.style.display = 'block';
        msg.textContent = message;
        panel.style.backgroundColor = type === 'success' ? 'rgba(0, 255, 136, 0.1)' :
                                     type === 'error' ? 'rgba(255, 51, 102, 0.1)' :
                                     type === 'warning' ? 'rgba(255, 170, 0, 0.1)' :
                                     'rgba(0, 212, 255, 0.1)';
        msg.style.color = type === 'success' ? '#00ff88' :
                         type === 'error' ? '#ff3366' :
                         type === 'warning' ? '#ffaa00' :
                         '#00d4ff';
        setTimeout(() => { panel.style.display = 'none'; }, 3000);
    }
}
```

## 📝 Field Label Pattern

```html
<div class="form-group">
    <label class="form-label" for="field_id" title="Tooltip description">Field Label *</label>
    <input type="text" class="form-input" id="field_id" name="field_id" required
           placeholder="Enter value..." title="Additional help text">
    <small style="color: #64748b; display: block; margin-top: 0.25rem;">Required: Help text for user</small>
</div>
```

## ✅ Checklist for Each Form/View

- [ ] Update title to include "- APDS"
- [ ] Add DMO operations panel
- [ ] Add DNO navigation panel
- [ ] Add feedback panel
- [ ] Update form fields with proper labels and tooltips
- [ ] Add hidden ID field
- [ ] Add `name="mainForm"` to form
- [ ] Initialize DMO/DNO JavaScript
- [ ] Implement loadRecords function
- [ ] Implement populateForm function
- [ ] Implement searchRecords function
- [ ] Implement showFeedback function
- [ ] Add tooltips to all controls
- [ ] Test all DMO operations
- [ ] Test all DNO operations
- [ ] Verify feedback messages work
- [ ] Verify help messages work

## 🎯 Key Requirements Summary

1. **Proper Controls**: All form fields have proper labels, titles, and validation
2. **DMO Operations**: Add, Edit, Delete, Save, Cancel, Search, Help, Refresh, Load Defaults
3. **DNO Operations**: First, Last, Previous, Next with record counter
4. **Feedback**: Visual feedback on all operations (success, error, warning, info)
5. **Support**: Tooltips on controls, help messages for operations
6. **APDS Branding**: All titles and headers updated to "APDS"

