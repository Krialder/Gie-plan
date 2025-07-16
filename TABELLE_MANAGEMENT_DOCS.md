# Tabelle Management - Documentation

## Overview

The **Tabelle Management** feature provides a user-friendly interface for creating and managing CSV files that contain the watering schedule in a format suitable for end users. This feature bridges the gap between the administrative generator (for the boss) and the practical schedule tables (for the users).

## Features

### 📊 **Two-Column Layout**
- **Left Column**: Shows the expected CSV structure based on current data
- **Right Column**: Shows the actual content of the existing CSV file

### 🎯 **User-Friendly CSV Format**
The CSV file contains the following columns:
- **Kalenderwoche** (Calendar Week): KW format (e.g., "KW 15")
- **Jahr** (Year): Four-digit year (e.g., "2025")
- **Datum** (Date): Date range for the week (e.g., "14.04 - 20.04")
- **Person 1**: First assigned person
- **Person 2**: Second assigned person
- **Ersatz 1**: First substitute person
- **Ersatz 2**: Second substitute person
- **Status**: Current status of the week

### 📋 **Status Indicators**
- **Aktuelle Woche** (Current Week): Highlighted in blue
- **Nächste Woche** (Next Week): Highlighted in orange
- **Vergangen** (Past): Grayed out
- **Zukünftig** (Future): Standard formatting

### 🔒 **File Protection**
- CSV files are automatically set to read-only for end users
- Only the generator application can modify the files
- Prevents accidental changes by users

## Functionality

### 📊 **Create/Update CSV Tabelle**
- Converts current schedule data into user-friendly CSV format
- Automatically names file based on current year (e.g., `giessplan_2025.csv`)
- Overwrites existing files with updated data
- Sets file permissions to read-only

### 📂 **Open CSV File**
- Opens the CSV file in the default application (usually Excel)
- Provides error handling if file doesn't exist
- Suggests creating the file if not found

### 🔄 **Refresh**
- Updates both preview displays
- Refreshes file status information
- Checks for file changes made outside the application

## User Interface

### Control Section
- **File Info**: Shows current CSV file path and status
- **Action Buttons**: Create/Update, Open, and Refresh buttons
- **Protection Notice**: Informs about read-only file protection

### Preview Areas
- **Expected Structure**: Shows how the CSV will look based on current data
- **Current CSV Content**: Shows actual content of existing CSV file
- **Color Coding**: Visual status indicators for different week states

## Technical Implementation

### File Naming Convention
- Format: `giessplan_YYYY.csv` (e.g., `giessplan_2025.csv`)
- Automatically updates when switching between years
- Separate files for each year

### Data Processing
- Extracts schedule data from existing watering history
- Converts internal format to user-friendly CSV structure
- Handles both main persons and substitute persons
- Calculates proper date ranges for each week

### Error Handling
- Graceful handling of missing files
- Permission error handling for read-only files
- Validation of data before CSV generation
- User-friendly error messages

## Usage Instructions

### For Administrators (Boss)
1. **Generate Schedule**: Use other tabs to create the watering schedule
2. **Create CSV**: Click "Create/Update CSV Tabelle" to generate user file
3. **Distribute**: Share the CSV file with end users
4. **Update**: Regenerate CSV whenever schedule changes

### For End Users
1. **Receive**: Get the CSV file from administrator
2. **Open**: Double-click to open in Excel or similar application
3. **View**: Check current and upcoming assignments
4. **Reference**: Use as reference for watering duties

## Integration

### With Existing System
- Seamlessly integrates with current GUI structure
- Uses existing theme and styling system
- Leverages existing data structures
- Maintains consistency with other tabs

### Theme Support
- Supports both RKI theme and basic fallback styling
- Consistent color scheme with rest of application
- Professional appearance matching organizational standards

## Benefits

### For Administrators
- **Easy Export**: One-click CSV generation
- **Consistent Format**: Standardized output format
- **File Protection**: Prevents user modifications
- **Year Management**: Automatic file naming by year

### For End Users
- **Readable Format**: Clear, understandable table structure
- **Excel Compatible**: Opens in familiar applications
- **Status Indicators**: Easy identification of current/upcoming weeks
- **Comprehensive Info**: All necessary details in one place

## File Structure

```
giessplan_2025.csv
├── Kalenderwoche (KW 15, KW 16, ...)
├── Jahr (2025)
├── Datum (14.04 - 20.04)
├── Person 1 (Main assignee)
├── Person 2 (Main assignee)
├── Ersatz 1 (First substitute)
├── Ersatz 2 (Second substitute)
└── Status (Current/Next/Past/Future)
```

## Troubleshooting

### Common Issues
1. **Permission Denied**: Close Excel before updating CSV
2. **File Not Found**: Create CSV first using the button
3. **Empty Display**: Check if schedule data exists
4. **Outdated Content**: Use Refresh button to update displays

### Best Practices
1. **Regular Updates**: Regenerate CSV after schedule changes
2. **Year Changes**: Switch years in main interface before generating CSV
3. **File Distribution**: Use proper file sharing methods for end users
4. **Backup**: Keep backup copies of generated CSV files

## Future Enhancements

### Potential Improvements
- Custom date range selection
- Email distribution integration
- Multiple export formats (PDF, etc.)
- Advanced filtering options
- Customizable column layouts

This documentation provides a comprehensive overview of the Tabelle Management feature, ensuring both administrators and end users can effectively utilize this functionality.
