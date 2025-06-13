var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

// // Double click callback for single grid
// dagfuncs.doubleClickCallback = function(params) {
//     console.log('Double click detected:', params);
    
//     // This will be automatically handled by Dash's built-in cellDoubleClicked callback
//     // No need for custom event handling since we're using the native AG Grid event
//     return true;
// };

// Row spanning function for single grid
dagfuncs.rowSpanningSimple = function(params) {
    var data = params.data;
    var field = params.column.colId;
    
    // Skip time column - no spanning
    if (field === 'time') {
        return 1;
    }
    
    // Check if this cell has an event and span value
    var spanField = field + '_span';
    if (data[field] && data[field].trim() !== '' && data[spanField]) {
        console.log('Row spanning for', field, 'at row', params.node.rowIndex, 'span:', data[spanField]);
        return data[spanField];
    }
    
    return 1;
};

// Generic cell style function that works for all day columns
dagfuncs.getCellStyle = function(params) {
    var value = params.value;
    var field = params.column.colId;  // This is already the day name
    
    // Skip styling for time column
    if (field === 'time') {
        return {
            'background-color': '#f8f9fa',
            'font-weight': '500',
            'text-align': 'center',
            'border-right': '2px solid #dee2e6'
        };
    }
    
    // Style for event cells
    if (value && value.trim() !== '') {
        var colorField = field + '_color';
        var color = params.data[colorField] || '#1fa22a';
        
        console.log('Applying style to', field, 'value:', value, 'color:', color, 'at row:', params.node.rowIndex);
        
        return {
            'background-color': color,
            'color': 'white',
            'border': '2px solid ' + color,
            'border-radius': '6px',
            'font-weight': 'bold',
            'text-align': 'center',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'cursor': 'pointer',
            'padding': '4px'
        };
    }
    
    // Default empty cell style
    return {
        'cursor': 'pointer',
        'border-right': '1px solid #dee2e6',
        'hover': {
            'background-color': '#f8f9fa'
        }
    };
};

// Make functions globally available
// window.doubleClickCallback = dagfuncs.doubleClickCallback;
window.rowSpanningSimple = dagfuncs.rowSpanningSimple;
window.getCellStyle = dagfuncs.getCellStyle; 