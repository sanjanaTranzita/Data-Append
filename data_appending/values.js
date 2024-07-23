const XLSX = require('xlsx');

const workbook = XLSX.readFile('Desireshop.xlsx');
const sheetName = 'Catalogue';  
const worksheet = workbook.Sheets[sheetName];

// Convert sheet to JSON array
let data = XLSX.utils.sheet_to_json(worksheet, { defval: null });

const removeUndefinedKey = (data, column) => {
    data.forEach((row) => {
        if (row[column]) {
            try {
                let variationImageMap = JSON.parse(row[column]);
                if ('undefined' in variationImageMap) {
                    delete variationImageMap['undefined'];
                    row[column] = JSON.stringify(variationImageMap);
                }
            } catch (e) {
                console.error(`Error parsing JSON for row ${JSON.stringify(row)}: ${e}`);
            }
        }
    });
};

removeUndefinedKey(data, 'variation_image_map');
const newWorksheet = XLSX.utils.json_to_sheet(data);

workbook.Sheets[sheetName] = newWorksheet;

// Write the updated workbook to a new file
XLSX.writeFile(workbook, 'Desireshop_updated.xlsx');
