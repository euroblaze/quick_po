Quick PurchaseOrder CSV Exporter

## Overview
This specificatoin describes the functional requirements for an Odoo v15 module to export line items from single or multiple PurchaseOrders (POs) into a CSV file with just two columns. The CSV can then be saved to the desktop. The module also features error checking for missing vendor article numbers and limits on batch exports to prevent performance degradation.

## Functional Requirements

### 1. Single Order Export

On a single order form view, the module will add an option under the Print menu to "Export Quick PurchaseOrder (CSV)". Upon clicking this option, the following actions occur:

- The module exports the line items from the purchase order to a CSV file. 
- The CSV includes two columns: Vendor Article Number and Quantity.
- If any line items in the order do not have a vendor article number, an error message is issued: "Following products do not have this supplier set up with an article number (and possibly other purchase related product information). Please fill this information in, and attempt to generate the Quick PO CSV again."
    - List the deficient products which do not have the supplier information.

### 2. Multiple Orders Export

From the list view, the module allows the selection of multiple POs for export. The behavior of the export function is identical to the single order export function described above. If multiple POs are selected, the line items from all selected orders are included in the exported CSV.

### 3. Export Limitations

The module issues a warning message if the user attempts to generate a QuickPO for more than 10 orders at a time. The warning message advises the user to perform the operation on 10 or fewer POs at a time to prevent performance degradation.

## Non-Functional Requirements

### 1. Language Support

All language labels in the module should be translatable to support internationalization.

### 2. Performance

The module should not negatively affect the performance of the Odoo v15 system, even when handling the maximum allowable batch size of 10 POs.
