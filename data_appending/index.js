const XLSX = require('xlsx');

const workbook = XLSX.readFile('overlap-6_updated.xlsx');
const sheetName = 'Catalogue';  
const worksheet = workbook.Sheets[sheetName];

let data = XLSX.utils.sheet_to_json(worksheet, { defval: null });

const fillMissingValues = (data, columns) => {
    let lastValues = {};
    columns.forEach(column => {
        lastValues[column] = null;
    });

    data.forEach((row) => {
        columns.forEach(column => {
            if (row[column] && row[column] !== 'NA') {
                lastValues[column] = row[column];
            } else {
                row[column] = lastValues[column];
            }
        });
    });
};

const removeUndefined = (data, column) => {
    data.forEach((row) => {
        if (row[column] === undefined) {
            row[column] = {}; 
        }
    });
};

const columnsToFill = ['flipkartCategory', 'super_category', 'category', 'sub_category', 'sub_sub_category', 'brand']; 
fillMissingValues(data, columnsToFill);

const newWorksheet = XLSX.utils.json_to_sheet(data);
workbook.Sheets[sheetName] = newWorksheet;
XLSX.writeFile(workbook, 'overlap-6.xlsx');

