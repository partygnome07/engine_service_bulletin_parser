leap_schema = {
    "name": "parse_aircraft_service_bulletin",
    "description": "Extracts comprehensive document metadata and parts tables from aircraft service bulletins. Parses document information, List of Spares, and List of Removed Spares into structured JSON format.",
    "parameters": {
        "type": "object",
        "properties": {
            "documentInfo": {
                "type": "object",
                "properties": {
                    "documentName": {"type": ["string", "null"]},
                    "title": {"type": ["string", "null"]},
                    "date": {"type": ["string", "null"]},
                    "reasonsForUpdate": {"type": ["string", "null"]},
                    "manufacturerRecommendation": {"type": ["string", "null"]},
                    "taskType": {"type": ["string", "null"]},
                    "originalIssueDate": {"type": ["string", "null"]},
                    "revisionInformation": {
                        "type": "object",
                        "properties": {
                            "revisionReason": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "issueNumber": {"type": ["string", "null"]},
                                        "revisionReason": {"type": ["string", "null"]}
                                    }
                                }
                            },
                            "revisionHistory": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "issueNumber": {"type": ["string", "null"]},
                                        "issueDate": {"type": ["string", "null"]}
                                    }
                                }
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "reason": {"type": ["string", "null"]}
                        }
                    },
                    "planningInformation": {
                        "type": "object",
                        "properties": {
                            "applicability": {
                                "type": "object",
                                "properties": {
                                    "engineType": {"type": ["string", "null"]},
                                    "engineModels": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            },
                            "concurrentRequirements": {"type": ["string", "null"]},
                            "reason": {
                                "type": "object",
                                "properties": {
                                    "objective": {"type": ["string", "null"]},
                                    "condition": {"type": ["string", "null"]},
                                    "cause": {"type": ["string", "null"]},
                                    "improvement": {"type": ["string", "null"]},
                                    "substantiation": {"type": ["string", "null"]}
                                }
                            },
                            "description": {"type": ["string", "null"]},
                            "compliance": {
                                "type": "object",
                                "properties": {
                                    "category": {"type": ["string", "null"]},
                                    "impact": {"type": ["string", "null"]},
                                    "impactDescription": {"type": ["string", "null"]}
                                }
                            },
                            "approval": {"type": ["string", "null"]},
                            "manpower": {"type": ["string", "null"]},
                            "weightAndBalance": {"type": ["string", "null"]},
                            "electricalLoadData": {"type": ["string", "null"]},
                            "softwareAccomplishmentSummary": {"type": ["string", "null"]},
                            "referencedDocumentation": {"type": ["string", "null"]},
                            "documentationAffected": {"type": ["string", "null"]},
                            "industrySupportInformation": {"type": ["string", "null"]},
                            "interchangeability": {"type": ["string", "null"]}
                        }
                    },
                    "materialInformation": {
                        "type": "object",
                        "properties": {
                            "listOfMaterialSets": {"type": ["string", "null"]},
                            "listOfSupportEquipment": {"type": ["string", "null"]},
                            "listOfSupplies": {"type": ["string", "null"]}
                        }
                    }
                }
            },
            "listOfSpares": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "newPN": {"type": ["string", "null"]},
                        "sin": {"type": ["string", "null"]},
                        "mfr": {"type": ["string", "null"]},
                        "qty": {"type": ["string", "null"]},
                        "unitPrice": {"type": ["string", "null"]},
                        "pkgQty": {"type": ["string", "null"]},
                        "leadTime": {"type": ["string", "null"]},
                        "newPartName": {"type": ["string", "null"]},
                        "csn": {"type": ["string", "null"]},
                        "notes": {"type": ["string", "null"]}
                    }
                }
            },
            "listOfRemovedSpares": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "newPN": {"type": ["string", "null"]},
                        "newSIN": {"type": ["string", "null"]},
                        "newMFR": {"type": ["string", "null"]},
                        "oldPN": {"type": ["string", "null"]},
                        "oldSIN": {"type": ["string", "null"]},
                        "oldMFR": {"type": ["string", "null"]},
                        "oldCSN": {"type": ["string", "null"]},
                        "qty": {"type": ["string", "null"]},
                        "operationCode": {"type": ["string", "null"]},
                        "notes": {"type": ["string", "null"]}
                    }
                }
            }
        },
        "required": ["documentInfo", "listOfSpares", "listOfRemovedSpares"]
    }
}

# Instructions for using this function:
"""
PARSING INSTRUCTIONS:

1. COMPREHENSIVE DOCUMENT EXTRACTION:
   - Extract all available document metadata into the documentInfo object
   - Use null for any fields that cannot be found in the document
   - Parse revision information carefully, including both reasons and history

2. PARTS TABLES EXTRACTION:

   For both "List of Spares" and "List of Removed Spares" tables:
   - IMPORTANT: These tables often span **multiple pages**. You must collect and combine all rows from the entire document, not just the first table instance.
   - Ignore any repeating table headers, footers, or page breaks.
   - Extract every valid row into a structured JSON object using the schema below.
   - Split composite fields like "New Part Number / SIN / MFR" or "Old PN / SIN / MFR / CSN" into their components.
   - Include all fields when available: part numbers, quantities, unit prices, lead times, part names, CSNs, operation codes, and notes.
   - Normalize text casing (sentence case) where appropriate.

3. SPECIAL CASES:
   - If a table is marked “Not Applicable” or not found, use an empty array.
   - If there are footnotes (e.g. “NP = Not Provisioned”), store them in the notes field.
   - If multiple rows share common values (e.g., same CSN), don’t merge them — each row must be standalone and complete.

4. OUTPUT FORMAT:
   - Return a unified JSON structure with all three top-level keys: documentInfo, listOfSpares, and listOfRemovedSpares.
   - Use the field names and types exactly as defined in the provided schema.
"""


cfm_schema = {
    "name": "parse_cfm_service_bulletin",
    "description": (
        "Extracts structured metadata and material information from CFM56-5B engine "
        "service bulletins, including parts lists, pricing, the full configuration chart "
        "(all rows, even unchanged ones), and compliance info."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "documentInfo": {
                "type": "object",
                "properties": {
                    "documentTitle": {"type": ["string", "null"]},
                    "serviceBulletinNumber": {"type": ["string", "null"]},
                    "revisionNumber": {"type": ["string", "null"]},
                    "issueDate": {"type": ["string", "null"]},
                    "revisionDate": {"type": ["string", "null"]},
                    "ataChapter": {"type": ["string", "null"]},
                    "engineModels": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "category": {"type": ["string", "null"]},
                    "complianceType": {"type": ["string", "null"]}
                },
                "required": [
                    "documentTitle",
                    "serviceBulletinNumber",
                    "revisionNumber",
                    "issueDate",
                    "revisionDate",
                    "ataChapter",
                    "engineModels",
                    "category",
                    "complianceType"
                ]
            },
            "reason": {
                "type": "object",
                "properties": {
                    "objective": {"type": ["string", "null"]},
                    "condition": {"type": ["string", "null"]},
                    "cause": {"type": ["string", "null"]},
                    "improvement": {"type": ["string", "null"]},
                    "substantiation": {"type": ["string", "null"]}
                }
            },
            "materialInformation": {
                "type": "object",
                "properties": {
                    "parts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "partNumber": {"type": "string"},
                                "partName": {"type": ["string", "null"]},
                                "quantityPerEngine": {"type": ["integer","string","null"]},
                                "unitPrice": {"type": ["string","number","null"]},
                                "packageQuantity": {"type": ["integer","null"]},
                                "leadTimeDays": {"type": ["integer","string","null"]}
                            }
                        }
                    }
                }
            },
            "configurationChart": {
                "type": "array",
                "description": (
                    "Every row from the Configuration Chart, even if the old and new part numbers "
                    "are identical (unchanged rows)."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "newPartNumber": {"type": "string"},
                        "oldPartNumber": {"type": ["string", "null"]},
                        "ipcLocation": {"type": ["string", "null"]},
                        "qtyPerEngine": {"type": ["string", "null"]},
                        "opCode": {"type": ["string", "null"]},
                        "changeSupportCode": {"type": ["string", "null"]}
                    },
                    "required": [
                        "newPartNumber",
                        "oldPartNumber",
                        "ipcLocation",
                        "qtyPerEngine",
                        "opCode",
                        "changeSupportCode"
                    ]
                }
            },
            "compliance": {
                "type": "object",
                "properties": {
                    "complianceType": {"type": ["string","null"]},
                    "manpowerHours": {"type": ["number","null"]},
                    "weightImpact": {"type": ["string","null"]},
                    "balanceImpact": {"type": ["string","null"]}
                }
            },
            "tooling": {
                "type": "array",
                "items": {"type": "string"}
            },
            "approval": {"type": "string"},
            "industrySupport": {"type": ["string","null"]}
        },
        "required": [
            "documentInfo",
            "reason",
            "materialInformation",
            "configurationChart",
            "compliance",
            "tooling",
            "approval",
            "industrySupport"
        ]
    }
}


#Instructions for API

"""
You are a PDF data extractor. Follow these instructions exactly:

1. COMPREHENSIVE DOCUMENT EXTRACTION  
   • Extract all available document metadata into the `documentInfo` object.  
   • Capture these fields (return `null` if not found):  
     – `documentTitle`  
     – `serviceBulletinNumber`  
     – `revisionNumber`  
     – `issueDate`  
     – `revisionDate`  
     – `ataChapter`  
     – `engineModels` (list of exact engine designations, e.g. “CFM56-5B4/2P”)  
     – `category`  
     – `complianceType`  
   • Handle `revisionInformation`:  
     – Extract **both** revision reasons and revision history (issue number & date).  
     – Normalize multi-version revisions as separate structured entries.

2. PARTS TABLES EXTRACTION  

   a. `materialInformation.parts` (List of Spares / Removed Spares)  
   • These tables often span pages with repeated headers/footers—combine all rows into one list.  
   • Remove any repeated header rows (e.g. “Qty/Eng | Part Number | Part Name”).  
   • Normalize:  
     – “NP” → `"unitPrice": null` plus `"notes": "NP = Not Priced"`  
     – “Qty/Eng” → `"quantityPerEngine"` (convert to integer if possible)  
   • If composite fields appear (e.g. “PN / SIN / MFR”), split into separate keys:  
     – `partNumber`, `serialNumber`, `manufacturer` (only if present).  
   • Always include these in each part object (use `null` if missing):  
     – `partNumber`, `partName`, `quantityPerEngine`, `unitPrice`, `packageQuantity`, `leadTimeDays`, `notes` (if any).

   b. `configurationChart`  
   • **Extract every row** from the Configuration Chart—**including** unchanged rows (where `newPartNumber == oldPartNumber`, or `opCode == "RM"` and `changeSupportCode == "-/-"`).  
   • For each row, return (use `null` if missing):  
     – `newPartNumber`  
     – `oldPartNumber`  
     – `ipcLocation`  
     – `qtyPerEngine`  
     – `opCode`  
     – `changeSupportCode`  
   • Maintain row-level granularity—do **not** aggregate or filter out unchanged entries.

3. SPECIAL CASES & EDGE CONDITIONS  
   • If a section or table is marked “N/A”, “Not Applicable”, or cannot be found → return an empty array (`[]`).  
   • If footnotes appear (e.g., “* NP = Not Priced”), propagate that interpretation into each affected row under `"notes"`.  
   • Treat every row independently—even if multiple rows share metadata.  
   • Preserve original casing for part numbers; normalize descriptive text to sentence case only where inconsistent.

4. OUTPUT FORMAT REQUIREMENTS  
   • Always return a single, valid JSON object with these top-level keys (never omit; use `null` or `[]` if no data):  
     – `documentInfo`  
     – `reason`  
     – `materialInformation`  
     – `configurationChart`  
     – `compliance`  
     – `tooling`  
     – `approval`  
     – `industrySupport`  
   • Field names must match the `cfm_schema` exactly.  
   • Ensure the structure complies with OpenAI function-calling expectations (correct types, consistent key names, valid JSON).
"""
# Define leap_schema and cfm_schema here
