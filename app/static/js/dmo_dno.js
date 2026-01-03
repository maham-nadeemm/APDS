/**
 * Data Manipulation Operations (DMO) and Data Navigation Operations (DNO) Utilities
 * Provides common functionality for all APDS interfaces
 */

// DMO Operations Manager
class DMOOperations {
    constructor(config = {}) {
        this.formId = config.formId || 'mainForm';
        this.apiEndpoint = config.apiEndpoint || '';
        this.onSave = config.onSave || null;
        this.onDelete = config.onDelete || null;
        this.onCancel = config.onCancel || null;
        this.onSearch = config.onSearch || null;
        this.onRefresh = config.onRefresh || null;
        this.onLoadDefaults = config.onLoadDefaults || null;
        this.onHelp = config.onHelp || null;
        this.currentRecordId = config.currentRecordId || null;
        this.isEditMode = config.isEditMode || false;
    }

    // Add new record
    add() {
        this.isEditMode = false;
        this.currentRecordId = null;
        
        // Clear the hidden ID field if it exists
        const idFieldNames = ['monitoring_id', 'fault_id', 'vendor_id', 'equipment_id', 'id'];
        for (const fieldName of idFieldNames) {
            const field = document.getElementById(fieldName);
            if (field) {
                field.value = '';
            }
        }
        
        this.clearForm();
        this.loadDefaults();
        this.showFeedback('Add mode: Please fill in the form to create a new record', 'info');
        this.updateButtonStates();
    }

    // Edit existing record
    edit(recordId) {
        // If no recordId provided, try to get it from form
        if (!recordId) {
            recordId = getSelectedRecordId();
        }
        
        if (!recordId) {
            this.showFeedback('No record selected for editing. Please select a record first or use navigation buttons.', 'error');
            return;
        }
        this.isEditMode = true;
        this.currentRecordId = recordId;
        
        // Set the record ID in the form's hidden field
        const idFieldNames = ['monitoring_id', 'fault_id', 'vendor_id', 'equipment_id', 'id'];
        for (const fieldName of idFieldNames) {
            const field = document.getElementById(fieldName);
            if (field) {
                field.value = recordId;
                break;
            }
        }
        
        this.loadRecord(recordId);
        this.showFeedback('Edit mode: Modify the form and click Save to update', 'info');
        this.updateButtonStates();
    }

    // Delete record
    async delete(recordId) {
        // If no recordId provided, try to get it from form
        if (!recordId) {
            recordId = getSelectedRecordId();
        }
        
        if (!recordId) {
            this.showFeedback('No record selected for deletion. Please select a record first or use navigation buttons.', 'error');
            return;
        }

        if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/${recordId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (result.success) {
                this.showFeedback('Record deleted successfully', 'success');
                // Clear form after deletion
                this.clearForm();
                this.isEditMode = false;
                this.currentRecordId = null;
                this.updateButtonStates();
                if (this.onDelete) {
                    this.onDelete(recordId);
                }
                this.refresh();
            } else {
                this.showFeedback(result.message || 'Error deleting record', 'error');
            }
        } catch (error) {
            this.showFeedback('Network error. Please try again.', 'error');
            console.error('Delete error:', error);
        }
    }

    // Save record (Add or Update)
    async save() {
        const form = document.getElementById(this.formId);
        if (!form) {
            this.showFeedback('Form not found', 'error');
            return;
        }

        // Validate form
        if (!form.checkValidity()) {
            form.reportValidity();
            this.showFeedback('Please fill in all required fields', 'error');
            return;
        }

        // Collect form data manually to handle numeric fields properly
        const jsonData = {};
        const formElements = form.elements;
        
        for (let i = 0; i < formElements.length; i++) {
            const field = formElements[i];
            
            // Skip buttons and fields without names
            if (!field.name || field.type === 'button' || field.type === 'submit') {
                continue;
            }
            
            // Handle different field types
            if (field.type === 'checkbox') {
                jsonData[field.name] = field.checked;
            } else if (field.type === 'number') {
                // Convert numeric fields to numbers
                const value = field.value.trim();
                if (value !== '') {
                    jsonData[field.name] = parseFloat(value) || value;
                }
            } else if (field.type === 'date') {
                // Keep date as string
                if (field.value) {
                    jsonData[field.name] = field.value;
                }
            } else {
                // Text, textarea, select
                if (field.value && field.value.trim() !== '') {
                    jsonData[field.name] = field.value.trim();
                }
            }
        }
        
        // Remove the ID field from data if it's empty (for new records)
        const idFieldName = Object.keys(jsonData).find(key => key.includes('_id') || key === 'id');
        if (idFieldName && (!jsonData[idFieldName] || jsonData[idFieldName] === '')) {
            delete jsonData[idFieldName];
        }

        try {
            const url = this.isEditMode && this.currentRecordId
                ? `${this.apiEndpoint}/${this.currentRecordId}`
                : this.apiEndpoint;
            const method = this.isEditMode && this.currentRecordId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            const result = await response.json();

            if (result.success) {
                const message = this.isEditMode ? 'Record updated successfully' : 'Record created successfully';
                this.showFeedback(message, 'success');
                if (this.onSave) {
                    this.onSave(result.data);
                }
                this.refresh();
            } else {
                this.showFeedback(result.message || 'Error saving record', 'error');
            }
        } catch (error) {
            this.showFeedback('Network error. Please try again.', 'error');
            console.error('Save error:', error);
        }
    }

    // Cancel operation
    cancel() {
        if (this.isEditMode) {
            this.loadRecord(this.currentRecordId);
        } else {
            this.clearForm();
        }
        this.showFeedback('Operation cancelled', 'info');
        if (this.onCancel) {
            this.onCancel();
        }
    }

    // Search records
    search(query) {
        if (this.onSearch) {
            this.onSearch(query);
        } else {
            this.showFeedback('Search functionality not configured', 'warning');
        }
    }

    // Refresh data
    refresh() {
        if (this.onRefresh) {
            this.onRefresh();
        } else {
            window.location.reload();
        }
        this.showFeedback('Data refreshed', 'success');
    }

    // Load default values
    loadDefaults() {
        if (this.onLoadDefaults) {
            this.onLoadDefaults();
        } else {
            // Default behavior: set today's date if date field exists
            const dateFields = document.querySelectorAll('input[type="date"]');
            dateFields.forEach(field => {
                if (!field.value) {
                    field.value = new Date().toISOString().split('T')[0];
                }
            });
        }
        this.showFeedback('Default values loaded', 'info');
    }

    // Show help
    help() {
        if (this.onHelp) {
            this.onHelp();
        } else {
            alert('Help: Use the form controls to add, edit, or delete records. Use navigation buttons to move between records.');
        }
    }

    // Helper methods
    clearForm() {
        const form = document.getElementById(this.formId);
        if (form) {
            form.reset();
        }
    }

    async loadRecord(recordId) {
        try {
            const response = await fetch(`${this.apiEndpoint}/${recordId}`);
            const result = await response.json();

            if (result.success && result.data) {
                this.populateForm(result.data);
            } else {
                this.showFeedback('Record not found', 'error');
            }
        } catch (error) {
            this.showFeedback('Error loading record', 'error');
            console.error('Load error:', error);
        }
    }

    populateForm(data) {
        const form = document.getElementById(this.formId);
        if (!form) return;

        for (const [key, value] of Object.entries(data)) {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = value;
                } else {
                    field.value = value || '';
                }
            }
        }
    }

    updateButtonStates() {
        // Enable/disable buttons based on mode
        const editBtn = document.getElementById('btnEdit');
        const deleteBtn = document.getElementById('btnDelete');
        const saveBtn = document.getElementById('btnSave');
        const cancelBtn = document.getElementById('btnCancel');

        if (saveBtn) {
            saveBtn.textContent = this.isEditMode ? 'Update' : 'Save';
        }
    }

    showFeedback(message, type = 'info') {
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
}

// DNO Operations Manager
class DNOOperations {
    constructor(config = {}) {
        this.records = config.records || [];
        this.currentIndex = config.currentIndex || -1;
        this.onNavigate = config.onNavigate || null;
        this.onRecordChange = config.onRecordChange || null;
    }

    // Navigate to first record
    first() {
        if (this.records.length === 0) {
            this.showFeedback('No records available', 'warning');
            return;
        }
        this.currentIndex = 0;
        this.loadRecord(this.records[this.currentIndex]);
        this.showFeedback(`Showing record 1 of ${this.records.length}`, 'info');
        this.updateNavigationButtons();
    }

    // Navigate to last record
    last() {
        if (this.records.length === 0) {
            this.showFeedback('No records available', 'warning');
            return;
        }
        this.currentIndex = this.records.length - 1;
        this.loadRecord(this.records[this.currentIndex]);
        this.showFeedback(`Showing record ${this.records.length} of ${this.records.length}`, 'info');
        this.updateNavigationButtons();
    }

    // Navigate to previous record
    previous() {
        if (this.records.length === 0) {
            this.showFeedback('No records available', 'warning');
            return;
        }
        if (this.currentIndex <= 0) {
            this.showFeedback('Already at the first record', 'warning');
            return;
        }
        this.currentIndex--;
        this.loadRecord(this.records[this.currentIndex]);
        this.showFeedback(`Showing record ${this.currentIndex + 1} of ${this.records.length}`, 'info');
        this.updateNavigationButtons();
    }

    // Navigate to next record
    next() {
        if (this.records.length === 0) {
            this.showFeedback('No records available', 'warning');
            return;
        }
        if (this.currentIndex >= this.records.length - 1) {
            this.showFeedback('Already at the last record', 'warning');
            return;
        }
        this.currentIndex++;
        this.loadRecord(this.records[this.currentIndex]);
        this.showFeedback(`Showing record ${this.currentIndex + 1} of ${this.records.length}`, 'info');
        this.updateNavigationButtons();
    }

    // Load record at current index
    loadRecord(record) {
        if (this.onRecordChange) {
            this.onRecordChange(record, this.currentIndex);
        }
        if (this.onNavigate) {
            this.onNavigate(record, this.currentIndex);
        }
    }

    // Update records list
    setRecords(records) {
        this.records = records;
        if (records.length > 0 && this.currentIndex === -1) {
            this.currentIndex = 0;
            this.loadRecord(records[0]);
        }
        this.updateNavigationButtons();
    }

    // Update navigation button states
    updateNavigationButtons() {
        const firstBtn = document.getElementById('btnFirst');
        const prevBtn = document.getElementById('btnPrevious');
        const nextBtn = document.getElementById('btnNext');
        const lastBtn = document.getElementById('btnLast');
        const recordInfo = document.getElementById('recordInfo');

        const hasRecords = this.records.length > 0;
        const isFirst = this.currentIndex <= 0;
        const isLast = this.currentIndex >= this.records.length - 1;

        if (firstBtn) firstBtn.disabled = !hasRecords || isFirst;
        if (prevBtn) prevBtn.disabled = !hasRecords || isFirst;
        if (nextBtn) nextBtn.disabled = !hasRecords || isLast;
        if (lastBtn) lastBtn.disabled = !hasRecords || isLast;

        if (recordInfo && hasRecords) {
            recordInfo.textContent = `Record ${this.currentIndex + 1} of ${this.records.length}`;
        } else if (recordInfo) {
            recordInfo.textContent = 'No records';
        }
    }

    showFeedback(message, type = 'info') {
        if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
}

// Support/Help System
class SupportSystem {
    constructor() {
        this.tooltips = new Map();
        this.helpContent = new Map();
    }

    // Add tooltip to control
    addTooltip(controlId, message) {
        const control = document.getElementById(controlId);
        if (control) {
            control.title = message;
            control.setAttribute('data-tooltip', message);
        }
        this.tooltips.set(controlId, message);
    }

    // Show help for control
    showControlHelp(controlId) {
        const help = this.helpContent.get(controlId) || this.tooltips.get(controlId);
        if (help) {
            alert(help);
        } else {
            alert('No help available for this control');
        }
    }

    // Show help for operation
    showOperationHelp(operation) {
        const helpMessages = {
            'add': 'Add: Click to create a new record. The form will be cleared and default values loaded.',
            'edit': 'Edit: Select a record and click Edit to modify its details.',
            'delete': 'Delete: Select a record and click Delete to remove it permanently. This action cannot be undone.',
            'save': 'Save: Click to save the current form data. If editing, the record will be updated. If adding, a new record will be created.',
            'cancel': 'Cancel: Click to cancel the current operation and revert changes.',
            'search': 'Search: Enter keywords to search for records matching your criteria.',
            'help': 'Help: Click to view help information for the current interface.',
            'refresh': 'Refresh: Click to reload data from the server.',
            'loadDefaults': 'Load Defaults: Click to populate the form with default values.',
            'first': 'First: Navigate to the first record in the list.',
            'last': 'Last: Navigate to the last record in the list.',
            'previous': 'Previous: Navigate to the previous record.',
            'next': 'Next: Navigate to the next record.'
        };

        const message = helpMessages[operation.toLowerCase()] || `Help for ${operation}: This operation is available in the current interface.`;
        alert(message);
    }
}

// Initialize DMO/DNO for a form
function initializeDMO_DNO(config) {
    const dmo = new DMOOperations(config.dmo || {});
    const dno = new DNOOperations(config.dno || {});
    const support = new SupportSystem();

    // Attach to window for global access
    window.dmo = dmo;
    window.dno = dno;
    window.support = support;

    // Setup button event listeners
    setupDMOButtons(dmo, support);
    setupDNOButtons(dno, support);

    return { dmo, dno, support };
}

// Setup DMO button listeners
function setupDMOButtons(dmo, support) {
    const btnAdd = document.getElementById('btnAdd');
    const btnEdit = document.getElementById('btnEdit');
    const btnDelete = document.getElementById('btnDelete');
    const btnSave = document.getElementById('btnSave');
    const btnCancel = document.getElementById('btnCancel');
    const btnSearch = document.getElementById('btnSearch');
    const btnHelp = document.getElementById('btnHelp');
    const btnRefresh = document.getElementById('btnRefresh');
    const btnLoadDefaults = document.getElementById('btnLoadDefaults');

    if (btnAdd) {
        btnAdd.addEventListener('click', () => {
            dmo.add();
            support.showOperationHelp('add');
        });
    }

    if (btnEdit) {
        btnEdit.addEventListener('click', () => {
            const recordId = getSelectedRecordId();
            dmo.edit(recordId);
            support.showOperationHelp('edit');
        });
    }

    if (btnDelete) {
        btnDelete.addEventListener('click', () => {
            const recordId = getSelectedRecordId();
            dmo.delete(recordId);
            support.showOperationHelp('delete');
        });
    }

    if (btnSave) {
        btnSave.addEventListener('click', () => {
            dmo.save();
            support.showOperationHelp('save');
        });
    }

    if (btnCancel) {
        btnCancel.addEventListener('click', () => {
            dmo.cancel();
            support.showOperationHelp('cancel');
        });
    }

    if (btnSearch) {
        btnSearch.addEventListener('click', () => {
            const query = document.getElementById('searchInput')?.value || '';
            dmo.search(query);
            support.showOperationHelp('search');
        });
    }

    if (btnHelp) {
        btnHelp.addEventListener('click', () => {
            dmo.help();
            support.showOperationHelp('help');
        });
    }

    if (btnRefresh) {
        btnRefresh.addEventListener('click', () => {
            dmo.refresh();
            support.showOperationHelp('refresh');
        });
    }

    if (btnLoadDefaults) {
        btnLoadDefaults.addEventListener('click', () => {
            dmo.loadDefaults();
            support.showOperationHelp('loadDefaults');
        });
    }
}

// Setup DNO button listeners
function setupDNOButtons(dno, support) {
    const btnFirst = document.getElementById('btnFirst');
    const btnPrevious = document.getElementById('btnPrevious');
    const btnNext = document.getElementById('btnNext');
    const btnLast = document.getElementById('btnLast');

    if (btnFirst) {
        btnFirst.addEventListener('click', () => {
            dno.first();
            support.showOperationHelp('first');
        });
    }

    if (btnPrevious) {
        btnPrevious.addEventListener('click', () => {
            dno.previous();
            support.showOperationHelp('previous');
        });
    }

    if (btnNext) {
        btnNext.addEventListener('click', () => {
            dno.next();
            support.showOperationHelp('next');
        });
    }

    if (btnLast) {
        btnLast.addEventListener('click', () => {
            dno.last();
            support.showOperationHelp('last');
        });
    }
}

// Helper function to get selected record ID
function getSelectedRecordId() {
    // Try multiple methods to get record ID
    // First, try common hidden field names
    const fieldNames = ['monitoring_id', 'fault_id', 'vendor_id', 'equipment_id', 'id'];
    for (const fieldName of fieldNames) {
        const field = document.getElementById(fieldName);
        if (field && field.value) {
            return field.value;
        }
    }
    
    // Try any hidden input with id containing "id"
    const hiddenId = document.querySelector('input[type="hidden"][id*="id"]');
    if (hiddenId && hiddenId.value) return hiddenId.value;

    // Try selected row in table
    const selectedRow = document.querySelector('tr.selected');
    if (selectedRow) {
        return selectedRow.getAttribute('data-id');
    }
    
    // Try currentRecordId from DMO
    if (window.dmo && window.dmo.currentRecordId) {
        return window.dmo.currentRecordId;
    }

    return null;
}

