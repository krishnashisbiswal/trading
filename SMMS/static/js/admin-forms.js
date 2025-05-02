/**
 * Common JavaScript for Admin Forms Handling
 * Arthavidya Trading Community
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeFormHandlers();
    initializeTableSearch();
    initializeFilterHandlers();
    initializeTableActions();
    initializePagination();
});

/**
 * Initialize form open/close handlers
 */
function initializeFormHandlers() {
    // Get the modal form elements
    const modalForms = document.querySelectorAll('.modal-form');
    if (!modalForms.length) return;
    
    // For each modal form on the page
    modalForms.forEach(form => {
        const formId = form.id;
        const formPrefix = formId.replace('Form', '');
        const addBtn = document.getElementById(`add${formPrefix.charAt(0).toUpperCase() + formPrefix.slice(1)}Btn`);
        const closeBtn = form.querySelector('.close-btn');
        const cancelBtn = form.querySelector('.cancel-btn');
        const dataForm = form.querySelector('form');
        
        // Open form when Add button is clicked
        if (addBtn) {
            addBtn.addEventListener('click', function() {
                const formTitle = form.querySelector('#formTitle');
                if (formTitle) {
                    formTitle.textContent = `Add New ${formPrefix.charAt(0).toUpperCase() + formPrefix.slice(1)}`;
                }
                if (dataForm) dataForm.reset();
                form.classList.add('active');
                
                // Reset any hidden inputs
                const hiddenInputs = dataForm.querySelectorAll('input[type="hidden"]');
                hiddenInputs.forEach(input => {
                    if (input.id !== 'formAction') {
                        input.value = '';
                    }
                });
                
                // Set form action to 'add'
                const formActionInput = dataForm.querySelector('#formAction');
                if (formActionInput) {
                    formActionInput.value = 'add';
                }
            });
        }
        
        // Close form when X button is clicked
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                form.classList.remove('active');
            });
        }
        
        // Close form when Cancel button is clicked
        if (cancelBtn) {
            cancelBtn.addEventListener('click', function() {
                form.classList.remove('active');
            });
        }
        
        // Close form when clicking outside
        form.addEventListener('click', function(e) {
            if (e.target === form) {
                form.classList.remove('active');
            }
        });
        
        // Submit form handler
        if (dataForm) {
            dataForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(dataForm);
                const formAction = formData.get('formAction') || 'add';
                
                // Here you would typically send the data to your backend
                console.log(`${formPrefix} form submitted with action: ${formAction}`);
                console.log('Form data:', Object.fromEntries(formData));
                
                // Show success message (in a real app, this would be after successful API call)
                alert(`${formPrefix.charAt(0).toUpperCase() + formPrefix.slice(1)} ${formAction === 'add' ? 'added' : 'updated'} successfully! In a real application, this would be saved to the database.`);
                
                // Close the form
                form.classList.remove('active');
            });
        }
    });
    
    // Handle edit buttons
    const editButtons = document.querySelectorAll('.action-btn.edit, .edit-recording');
    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Find the closest modal form based on the edited item type
            let modalForm;
            let formPrefix;
            const row = this.closest('tr');
            const card = this.closest('.category-card, .recording-card');
            
            if (row) {
                // Table row edit
                const tableName = this.closest('table').id;
                formPrefix = tableName.replace('Table', '').slice(0, -1); // Remove 's' from plural
                modalForm = document.getElementById(`${formPrefix}Form`);
            } else if (card) {
                // Card edit
                if (card.classList.contains('category-card')) {
                    formPrefix = 'category';
                } else if (card.classList.contains('recording-card')) {
                    formPrefix = 'recording';
                } else {
                    formPrefix = '';
                }
                modalForm = document.getElementById(`${formPrefix}Form`);
            }
            
            if (!modalForm) return;
            
            // Update form title
            const formTitle = modalForm.querySelector('#formTitle');
            if (formTitle) {
                formTitle.textContent = `Edit ${formPrefix.charAt(0).toUpperCase() + formPrefix.slice(1)}`;
            }
            
            // Set form action to 'edit'
            const formActionInput = modalForm.querySelector('#formAction');
            if (formActionInput) {
                formActionInput.value = 'edit';
            }
            
            // Extract data from the row or card and populate the form
            if (row) {
                populateFormFromTableRow(row, modalForm, formPrefix);
            } else if (card) {
                populateFormFromCard(card, modalForm, formPrefix);
            }
            
            // Open the form
            modalForm.classList.add('active');
        });
    });
    
    // Handle delete buttons
    const deleteButtons = document.querySelectorAll('.action-btn.delete, .delete-recording');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            let itemName = '';
            const row = this.closest('tr');
            const card = this.closest('.category-card, .recording-card');
            
            if (row) {
                itemName = row.cells[0].textContent;
            } else if (card) {
                const titleElem = card.querySelector('.category-title, .recording-title');
                if (titleElem) itemName = titleElem.textContent;
            }
            
            if (confirm(`Are you sure you want to delete "${itemName}"?`)) {
                // Here you would typically send a delete request to your backend
                console.log(`Delete request for: ${itemName}`);
                alert(`Item deleted successfully! In a real application, this would be removed from the database.`);
                
                // Remove the row or card from the DOM (for demonstration)
                if (row) row.remove();
                if (card) card.remove();
            }
        });
    });
    
    // Initialize any special form elements
    initializeSpecialFormElements();
}

/**
 * Initialize special form elements (icon selection, multi-select, etc.)
 */
function initializeSpecialFormElements() {
    // Icon selection in category form
    const iconOptions = document.querySelectorAll('.icon-option');
    if (iconOptions.length) {
        iconOptions.forEach(option => {
            option.addEventListener('click', function() {
                // Remove selected class from all options
                iconOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Add selected class to clicked option
                this.classList.add('selected');
                
                // Update the hidden input value
                const iconInput = document.getElementById('selectedIcon');
                if (iconInput) {
                    iconInput.value = this.getAttribute('data-icon');
                }
            });
        });
    }
    
    // Handle visibility toggle in recording cards
    const visibilitySwitches = document.querySelectorAll('.visibility-switch input');
    visibilitySwitches.forEach(switchInput => {
        switchInput.addEventListener('change', function() {
            const card = this.closest('.recording-card');
            const statusText = this.closest('.recording-visibility').querySelector('span');
            
            if (this.checked) {
                statusText.textContent = 'Visible';
            } else {
                statusText.textContent = 'Hidden';
            }
            
            // Here you would typically send an update to your backend
            console.log(`Recording visibility updated to: ${this.checked ? 'Visible' : 'Hidden'}`);
        });
    });
}

/**
 * Populate form from table row data
 */
function populateFormFromTableRow(row, form, formPrefix) {
    // Get all the cell values from the row
    const cells = Array.from(row.cells);
    const formId = `${formPrefix}Id`;
    
    // Set the ID for the form (usually a hidden input)
    const idInput = form.querySelector(`#${formId}`);
    if (idInput) {
        // In a real app, you would get the actual ID from a data attribute
        idInput.value = row.getAttribute('data-id') || '1';
    }
    
    // Specific form population based on prefix
    switch(formPrefix) {
        case 'batch':
            populateBatchForm(cells, form);
            break;
        case 'schedule':
            populateScheduleForm(cells, form);
            break;
        case 'category':
            populateCategoryForm(cells, form);
            break;
        case 'recording':
            populateRecordingForm(cells, form);
            break;
        default:
            // Generic form population
            const inputs = form.querySelectorAll('input:not([type="hidden"]), select, textarea');
            inputs.forEach((input, index) => {
                if (index < cells.length && cells[index].textContent) {
                    input.value = cells[index].textContent.trim();
                }
            });
    }
}

/**
 * Populate form from card data
 */
function populateFormFromCard(card, form, formPrefix) {
    // Set the ID for the form (usually a hidden input)
    const idInput = form.querySelector(`#${formPrefix}Id`);
    if (idInput) {
        // In a real app, you would get the actual ID from a data attribute
        idInput.value = card.getAttribute('data-id') || '1';
    }
    
    // Specific form population based on prefix
    switch(formPrefix) {
        case 'category':
            const categoryTitle = card.querySelector('.category-title');
            const categoryDesc = card.querySelector('.category-description');
            const categoryIcon = card.querySelector('.category-icon i');
            
            if (categoryTitle) {
                const titleInput = form.querySelector('#categoryName');
                if (titleInput) titleInput.value = categoryTitle.textContent;
            }
            
            if (categoryDesc) {
                const descInput = form.querySelector('#description');
                if (descInput) descInput.value = categoryDesc.textContent;
            }
            
            if (categoryIcon) {
                const iconClass = categoryIcon.className;
                const iconName = iconClass.replace('fas fa-', '');
                
                // Select the matching icon in the form
                const iconOptions = form.querySelectorAll('.icon-option');
                iconOptions.forEach(option => {
                    option.classList.remove('selected');
                    if (option.getAttribute('data-icon') === iconName) {
                        option.classList.add('selected');
                        
                        const iconInput = form.querySelector('#selectedIcon');
                        if (iconInput) iconInput.value = iconName;
                    }
                });
            }
            break;
        
        case 'recording':
            const recordingTitle = card.querySelector('.recording-title');
            const recordingInfo = card.querySelector('.recording-info');
            const visibilitySwitch = card.querySelector('.visibility-switch input');
            
            if (recordingTitle) {
                const titleInput = form.querySelector('#recordingTitle');
                if (titleInput) titleInput.value = recordingTitle.textContent;
            }
            
            if (recordingInfo) {
                const programInfo = recordingInfo.querySelector('span:nth-child(1)');
                const batchInfo = recordingInfo.querySelector('span:nth-child(2)');
                const trainerInfo = recordingInfo.querySelector('span:nth-child(3)');
                const dateInfo = recordingInfo.querySelector('span:nth-child(4)');
                
                if (programInfo) {
                    const programSelect = form.querySelector('#program');
                    if (programSelect) {
                        const programName = programInfo.textContent.replace(/^\s*\S+\s+/, ''); // Remove icon text
                        selectOptionByText(programSelect, programName);
                    }
                }
                
                if (batchInfo) {
                    const batchSelect = form.querySelector('#batch');
                    if (batchSelect) {
                        const batchName = batchInfo.textContent.replace(/^\s*\S+\s+/, ''); // Remove icon text
                        selectOptionByText(batchSelect, batchName);
                    }
                }
                
                if (trainerInfo) {
                    const trainerSelect = form.querySelector('#trainer');
                    if (trainerSelect) {
                        const trainerName = trainerInfo.textContent.replace(/^\s*\S+\s+/, ''); // Remove icon text
                        selectOptionByText(trainerSelect, trainerName);
                    }
                }
                
                if (dateInfo) {
                    const dateInput = form.querySelector('#recordingDate');
                    if (dateInput) {
                        const dateText = dateInfo.textContent.replace(/^\s*\S+\s+/, ''); // Remove icon text
                        // Convert date format from "April 1, 2025" to "2025-04-01"
                        const dateParts = new Date(dateText);
                        if (!isNaN(dateParts.getTime())) {
                            const formattedDate = dateParts.toISOString().split('T')[0];
                            dateInput.value = formattedDate;
                        }
                    }
                }
            }
            
            if (visibilitySwitch) {
                const visibleCheckbox = form.querySelector('#isVisible');
                if (visibleCheckbox) {
                    visibleCheckbox.checked = visibilitySwitch.checked;
                }
            }
            
            // Set dummy values for URL and duration fields
            const urlInput = form.querySelector('#recordingURL');
            if (urlInput) urlInput.value = 'https://example.com/recording.mp4';
            
            const durationInput = form.querySelector('#duration');
            const durationText = card.querySelector('.recording-duration');
            if (durationInput && durationText) {
                durationInput.value = durationText.textContent;
            } else if (durationInput) {
                durationInput.value = '01:30:00';
            }
            break;
            
        default:
            console.log('No specific form population for this card type');
    }
}

/**
 * Helper function to select an option in a select element by its text
 */
function selectOptionByText(selectElement, optionText) {
    for (let i = 0; i < selectElement.options.length; i++) {
        if (selectElement.options[i].text === optionText) {
            selectElement.selectedIndex = i;
            break;
        }
    }
}

/**
 * Batch form specific population
 */
function populateBatchForm(cells, form) {
    if (cells.length < 6) return;
    
    form.querySelector('#batchCode').value = cells[0].textContent.trim();
    form.querySelector('#batchName').value = cells[1].textContent.trim();
    
    // Set program dropdown
    const programSelect = form.querySelector('#program');
    selectOptionByText(programSelect, cells[2].textContent.trim());
    
    // Set dates
    const startDateInput = form.querySelector('#startDate');
    const endDateInput = form.querySelector('#endDate');
    
    if (startDateInput && cells[3]) {
        const startDateText = cells[3].textContent.trim();
        const startDateParts = new Date(startDateText);
        if (!isNaN(startDateParts.getTime())) {
            startDateInput.value = startDateParts.toISOString().split('T')[0];
        }
    }
    
    if (endDateInput && cells[4]) {
        const endDateText = cells[4].textContent.trim();
        const endDateParts = new Date(endDateText);
        if (!isNaN(endDateParts.getTime())) {
            endDateInput.value = endDateParts.toISOString().split('T')[0];
        }
    }
    
    // Set capacity
    const capacityInput = form.querySelector('#capacity');
    if (capacityInput && cells[5]) {
        capacityInput.value = cells[5].textContent.trim();
    }
    
    // Set status dropdown
    const statusSelect = form.querySelector('#status');
    if (statusSelect && cells[7]) {
        const statusText = cells[7].querySelector('.status-badge').textContent.trim().toLowerCase();
        for (let i = 0; i < statusSelect.options.length; i++) {
            if (statusSelect.options[i].value.toLowerCase() === statusText) {
                statusSelect.selectedIndex = i;
                break;
            }
        }
    }
}

/**
 * Schedule form specific population
 */
function populateScheduleForm(cells, form) {
    if (cells.length < 6) return;
    
    // Set class topic
    const topicInput = form.querySelector('#topic');
    if (topicInput && cells[4]) {
        topicInput.value = cells[4].textContent.trim();
    }
    
    // Set program dropdown
    const programSelect = form.querySelector('#program');
    if (programSelect && cells[2]) {
        selectOptionByText(programSelect, cells[2].textContent.trim());
    }
    
    // Set batch dropdown
    const batchSelect = form.querySelector('#batch');
    if (batchSelect && cells[3]) {
        selectOptionByText(batchSelect, cells[3].textContent.trim());
    }
    
    // Set trainer dropdown
    const trainerSelect = form.querySelector('#trainer');
    if (trainerSelect && cells[5]) {
        selectOptionByText(trainerSelect, cells[5].textContent.trim());
    }
    
    // Set date
    const dateInput = form.querySelector('#classDate');
    if (dateInput && cells[0]) {
        const dateText = cells[0].textContent.trim();
        const dateParts = new Date(dateText);
        if (!isNaN(dateParts.getTime())) {
            dateInput.value = dateParts.toISOString().split('T')[0];
        }
    }
    
    // Set times
    const timeText = cells[1] ? cells[1].textContent.trim() : '';
    const timeMatch = timeText.match(/(\d+:\d+)\s*([AP]M)\s*-\s*(\d+:\d+)\s*([AP]M)/i);
    
    if (timeMatch) {
        const startTimeInput = form.querySelector('#startTime');
        const endTimeInput = form.querySelector('#endTime');
        
        if (startTimeInput) {
            // Convert from "10:00 AM" to "10:00"
            let startHour = parseInt(timeMatch[1].split(':')[0]);
            const startMinute = timeMatch[1].split(':')[1];
            const startPeriod = timeMatch[2].toUpperCase();
            
            if (startPeriod === 'PM' && startHour < 12) startHour += 12;
            if (startPeriod === 'AM' && startHour === 12) startHour = 0;
            
            startTimeInput.value = `${startHour.toString().padStart(2, '0')}:${startMinute}`;
        }
        
        if (endTimeInput) {
            // Convert from "12:00 PM" to "12:00"
            let endHour = parseInt(timeMatch[3].split(':')[0]);
            const endMinute = timeMatch[3].split(':')[1];
            const endPeriod = timeMatch[4].toUpperCase();
            
            if (endPeriod === 'PM' && endHour < 12) endHour += 12;
            if (endPeriod === 'AM' && endHour === 12) endHour = 0;
            
            endTimeInput.value = `${endHour.toString().padStart(2, '0')}:${endMinute}`;
        }
    }
}

/**
 * Category form specific population
 */
function populateCategoryForm(cells, form) {
    if (cells.length < 3) return;
    
    // Set name and description
    form.querySelector('#categoryName').value = cells[0].textContent.trim();
    form.querySelector('#description').value = cells[1].textContent.trim();
    
    // Set icon
    const iconElement = cells[2].querySelector('i');
    if (iconElement) {
        const iconClass = iconElement.className;
        const iconName = iconClass.replace('fas fa-', '');
        
        // Select the matching icon in the form
        const iconOptions = form.querySelectorAll('.icon-option');
        iconOptions.forEach(option => {
            option.classList.remove('selected');
            if (option.getAttribute('data-icon') === iconName) {
                option.classList.add('selected');
                
                const iconInput = form.querySelector('#selectedIcon');
                if (iconInput) iconInput.value = iconName;
            }
        });
    }
}

/**
 * Recording form specific population
 */
function populateRecordingForm(cells, form) {
    if (cells.length < 6) return;
    
    // Set title
    form.querySelector('#recordingTitle').value = cells[0].textContent.trim();
    
    // Set program dropdown
    const programSelect = form.querySelector('#program');
    selectOptionByText(programSelect, cells[1].textContent.trim());
    
    // Set batch dropdown
    const batchSelect = form.querySelector('#batch');
    selectOptionByText(batchSelect, cells[2].textContent.trim());
    
    // Set trainer dropdown
    const trainerSelect = form.querySelector('#trainer');
    selectOptionByText(trainerSelect, cells[3].textContent.trim());
    
    // Set date
    const dateInput = form.querySelector('#recordingDate');
    if (dateInput && cells[4]) {
        const dateText = cells[4].textContent.trim();
        const dateParts = new Date(dateText);
        if (!isNaN(dateParts.getTime())) {
            dateInput.value = dateParts.toISOString().split('T')[0];
        }
    }
    
    // Set duration
    const durationInput = form.querySelector('#duration');
    if (durationInput && cells[5]) {
        durationInput.value = cells[5].textContent.trim();
    }
    
    // Set visibility checkbox
    const visibleCheckbox = form.querySelector('#isVisible');
    if (visibleCheckbox && cells[6]) {
        const statusText = cells[6].querySelector('.status-badge').textContent.trim().toLowerCase();
        visibleCheckbox.checked = (statusText === 'visible');
    }
    
    // Set dummy URL
    const urlInput = form.querySelector('#recordingURL');
    if (urlInput) {
        urlInput.value = 'https://example.com/recording.mp4';
    }
}

/**
 * Initialize table search functionality
 */
function initializeTableSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const targetTable = this.closest('.table-container').querySelector('table');
            
            if (!targetTable) return;
            
            const tableRows = targetTable.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchText) ? '' : 'none';
            });
        });
    });
}

/**
 * Initialize filter functionality
 */
function initializeFilterHandlers() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const filterDropdowns = document.querySelectorAll('.filter-dropdown');
    const applyFilterBtns = document.querySelectorAll('#applyFilterBtn');
    const resetFilterBtns = document.querySelectorAll('#resetFilterBtn');
    
    // Toggle filter dropdown
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('filter-dropdown')) {
                dropdown.classList.toggle('show');
            }
        });
    });
    
    // Close filter dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.filter-container')) {
            filterDropdowns.forEach(dropdown => {
                dropdown.classList.remove('show');
            });
        }
    });
    
    // Apply filter
    applyFilterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const dropdown = this.closest('.filter-dropdown');
            const tableContainer = dropdown.closest('.table-container');
            
            if (!tableContainer) return;
            
            const filterSelects = dropdown.querySelectorAll('select');
            const tableRows = tableContainer.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                let show = true;
                
                filterSelects.forEach(select => {
                    if (select.value) {
                        const filterColumn = select.id.replace('Filter', '');
                        let columnIndex = -1;
                        
                        // Find column index based on header text
                        const headers = tableContainer.querySelectorAll('thead th');
                        headers.forEach((header, index) => {
                            if (header.textContent.toLowerCase().includes(filterColumn.toLowerCase())) {
                                columnIndex = index;
                            }
                        });
                        
                        if (columnIndex > -1) {
                            const cellText = row.cells[columnIndex].textContent.toLowerCase();
                            const filterText = select.options[select.selectedIndex].text.toLowerCase();
                            
                            if (!cellText.includes(filterText)) {
                                show = false;
                            }
                        }
                    }
                });
                
                row.style.display = show ? '' : 'none';
            });
            
            dropdown.classList.remove('show');
        });
    });
    
    // Reset filter
    resetFilterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const dropdown = this.closest('.filter-dropdown');
            const filterSelects = dropdown.querySelectorAll('select');
            
            filterSelects.forEach(select => {
                select.selectedIndex = 0;
            });
            
            const tableContainer = dropdown.closest('.table-container');
            if (tableContainer) {
                const tableRows = tableContainer.querySelectorAll('tbody tr');
                tableRows.forEach(row => {
                    row.style.display = '';
                });
            }
        });
    });
}

/**
 * Initialize table actions (bulk actions, checkboxes)
 */
function initializeTableActions() {
    const selectAllCheckboxes = document.querySelectorAll('#selectAll');
    const bulkActions = document.querySelectorAll('#bulkActions');
    
    selectAllCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const table = this.closest('table');
            const rowCheckboxes = table.querySelectorAll('.rowCheckbox');
            
            rowCheckboxes.forEach(rowCheckbox => {
                rowCheckbox.checked = this.checked;
            });
            
            // Show/hide bulk actions
            const bulkAction = this.closest('.table-container').querySelector('#bulkActions');
            if (bulkAction) {
                if (this.checked) {
                    bulkAction.classList.add('show');
                    updateSelectedCount(bulkAction, rowCheckboxes.length);
                } else {
                    bulkAction.classList.remove('show');
                }
            }
        });
    });
    
    // Individual row checkboxes
    const rowCheckboxes = document.querySelectorAll('.rowCheckbox');
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const table = this.closest('table');
            const allCheckboxes = table.querySelectorAll('.rowCheckbox');
            const checkedCheckboxes = table.querySelectorAll('.rowCheckbox:checked');
            const selectAll = table.querySelector('#selectAll');
            
            if (selectAll) {
                selectAll.checked = checkedCheckboxes.length === allCheckboxes.length;
                selectAll.indeterminate = checkedCheckboxes.length > 0 && checkedCheckboxes.length < allCheckboxes.length;
            }
            
            // Show/hide bulk actions
            const bulkAction = this.closest('.table-container').querySelector('#bulkActions');
            if (bulkAction) {
                if (checkedCheckboxes.length > 0) {
                    bulkAction.classList.add('show');
                    updateSelectedCount(bulkAction, checkedCheckboxes.length);
                } else {
                    bulkAction.classList.remove('show');
                }
            }
        });
    });
    
    // Bulk action buttons
    const bulkDeleteBtns = document.querySelectorAll('.bulk-btn.delete');
    bulkDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const table = this.closest('.table-container').querySelector('table');
            const checkedCheckboxes = table.querySelectorAll('.rowCheckbox:checked');
            
            if (confirm(`Are you sure you want to delete ${checkedCheckboxes.length} items?`)) {
                // Here you would typically send a delete request to your backend
                console.log(`Bulk delete request for ${checkedCheckboxes.length} items`);
                alert(`Items deleted successfully! In a real application, these would be removed from the database.`);
                
                // Remove the rows from the DOM (for demonstration)
                checkedCheckboxes.forEach(checkbox => {
                    const row = checkbox.closest('tr');
                    if (row) row.remove();
                });
                
                // Hide bulk actions
                const bulkAction = this.closest('#bulkActions');
                if (bulkAction) {
                    bulkAction.classList.remove('show');
                }
                
                // Uncheck select all
                const selectAll = table.querySelector('#selectAll');
                if (selectAll) {
                    selectAll.checked = false;
                    selectAll.indeterminate = false;
                }
            }
        });
    });
}

/**
 * Update selected count in bulk actions
 */
function updateSelectedCount(bulkAction, count) {
    const selectedCount = bulkAction.querySelector('#selectedCount');
    if (selectedCount) {
        selectedCount.textContent = count;
    }
}

/**
 * Initialize pagination
 */
function initializePagination() {
    const prevPageBtns = document.querySelectorAll('#prevPage');
    const nextPageBtns = document.querySelectorAll('#nextPage');
    const pageBtns = document.querySelectorAll('.pagination .page-btn:not(#prevPage):not(#nextPage)');
    
    // Previous page
    prevPageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            
            const pagination = this.closest('.pagination');
            const activePage = pagination.querySelector('.page-btn.active');
            
            if (activePage && activePage.previousElementSibling && !activePage.previousElementSibling.id) {
                activePage.classList.remove('active');
                activePage.previousElementSibling.classList.add('active');
                
                // Update disabled state
                if (activePage.previousElementSibling.previousElementSibling && activePage.previousElementSibling.previousElementSibling.id === 'prevPage') {
                    this.disabled = true;
                }
                
                // Enable next button
                const nextBtn = pagination.querySelector('#nextPage');
                if (nextBtn) {
                    nextBtn.disabled = false;
                }
                
                // Update table data (in a real app, this would fetch new data)
                console.log('Previous page clicked');
            }
        });
    });
    
    // Next page
    nextPageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            
            const pagination = this.closest('.pagination');
            const activePage = pagination.querySelector('.page-btn.active');
            
            if (activePage && activePage.nextElementSibling && !activePage.nextElementSibling.id) {
                activePage.classList.remove('active');
                activePage.nextElementSibling.classList.add('active');
                
                // Update disabled state
                if (activePage.nextElementSibling.nextElementSibling && activePage.nextElementSibling.nextElementSibling.id === 'nextPage') {
                    this.disabled = true;
                }
                
                // Enable prev button
                const prevBtn = pagination.querySelector('#prevPage');
                if (prevBtn) {
                    prevBtn.disabled = false;
                }
                
                // Update table data (in a real app, this would fetch new data)
                console.log('Next page clicked');
            }
        });
    });
    
    // Page numbers
    pageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const pagination = this.closest('.pagination');
            const activePage = pagination.querySelector('.page-btn.active');
            
            if (activePage) {
                activePage.classList.remove('active');
            }
            
            this.classList.add('active');
            
            // Update prev/next disabled state
            const prevBtn = pagination.querySelector('#prevPage');
            const nextBtn = pagination.querySelector('#nextPage');
            
            if (prevBtn) {
                prevBtn.disabled = !this.previousElementSibling || this.previousElementSibling.id === 'prevPage';
            }
            
            if (nextBtn) {
                nextBtn.disabled = !this.nextElementSibling || this.nextElementSibling.id === 'nextPage';
            }
            
            // Update table data (in a real app, this would fetch new data)
            console.log(`Page ${this.textContent} clicked`);
        });
    });
}