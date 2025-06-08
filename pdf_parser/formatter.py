import pandas as pd
from io import BytesIO

def build_excel_output(result: dict, engine_type: str) -> tuple[BytesIO, pd.DataFrame]:
    output = BytesIO()

    if engine_type == "leap":
        doc = result.get("documentInfo", {})
        plan = doc.get("planningInformation", {})
        rev  = doc.get("revisionInformation", {})

        # metadata
        meta = {
            "Document Name":           doc.get("documentName"),
            "Title":                   doc.get("title"),
            "Date":                    doc.get("date"),
            "Reasons for Update":      doc.get("reasonsForUpdate"),
            "Manufacturer Recommendation": doc.get("manufacturerRecommendation"),
            "Task Type":               doc.get("taskType"),
            "Original Issue Date":     doc.get("originalIssueDate"),
            "Revision Issue#":         rev.get("revisionReason", [{}])[0].get("issueNumber"),
            "Revision Text":           rev.get("revisionReason", [{}])[0].get("revisionReason"),
            "Summary Reason":          doc.get("summary", {}).get("reason"),
            "Engine Type":             plan.get("applicability", {}).get("engineType"),
            "Engine Models":           ", ".join(plan.get("applicability", {}).get("engineModels", [])),
            "Objective":               plan.get("reason", {}).get("objective"),
            "Condition":               plan.get("reason", {}).get("condition"),
            "Cause":                   plan.get("reason", {}).get("cause"),
            "Improvement":             plan.get("reason", {}).get("improvement"),
            "Substantiation":          plan.get("reason", {}).get("substantiation"),
            "Compliance Category":     plan.get("compliance", {}).get("category"),
            "Compliance Impact":       plan.get("compliance", {}).get("impact"),
        }
        meta_df = pd.DataFrame([meta])

        spares = doc.get("listOfSpares") or doc.get("materialInformation", {}).get("listOfSpares", [])
        removed = doc.get("listOfRemovedSpares") or doc.get("materialInformation", {}).get("listOfRemovedSpares", [])
        spares_df  = pd.DataFrame(spares) if isinstance(spares, list) else pd.DataFrame()
        removed_df = pd.DataFrame(removed) if isinstance(removed, list) else pd.DataFrame()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            meta_df.to_excel(writer, sheet_name="Metadata", index=False)
            if not spares_df.empty:
                spares_df.to_excel(writer, sheet_name="ListOfSpares", index=False)
            if not removed_df.empty:
                removed_df.to_excel(writer, sheet_name="RemovedSpares", index=False)

        return output, spares_df

    else:  # CFM
        doc = result.get("documentInfo", {})
        reason = result.get("reason", {})
        comp   = result.get("compliance", {})
        mat    = result.get("materialInformation", {})
        cfg    = result.get("configurationChart", [])

        meta = {
            "Document Title":           doc.get("documentTitle"),
            "Service Bulletin #":       doc.get("serviceBulletinNumber"),
            "Revision #":               doc.get("revisionNumber"),
            "Issue Date":               doc.get("issueDate"),
            "Revision Date":            doc.get("revisionDate"),
            "ATA Chapter":              doc.get("ataChapter"),
            "Engine Models":            ", ".join(doc.get("engineModels", [])),
            "Category":                 doc.get("category"),
            "Compliance Type":          doc.get("complianceType"),
            "Objective":                reason.get("objective"),
            "Condition":                reason.get("condition"),
            "Cause":                    reason.get("cause"),
            "Improvement":              reason.get("improvement"),
            "Substantiation":           reason.get("substantiation"),
            "Manpower Hours":           comp.get("manpowerHours"),
            "Weight Impact":            comp.get("weightImpact"),
            "Balance Impact":           comp.get("balanceImpact"),
        }
        meta_df = pd.DataFrame([meta])

        parts_df = pd.DataFrame(mat.get("parts", []))
        cfg_df   = pd.DataFrame(cfg)

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            meta_df.to_excel(writer, sheet_name="Metadata", index=False)
            if not parts_df.empty:
                parts_df.insert(0, "SB Number", doc.get("serviceBulletinNumber"))
                parts_df.to_excel(writer, sheet_name="PartsList", index=False)
            if not cfg_df.empty:
                cfg_df.insert(0, "SB Number", doc.get("serviceBulletinNumber"))
                cfg_df.to_excel(writer, sheet_name="ConfigChanges", index=False)

        return output, parts_df
# Functions to build LEAP and CFM DataFrames from JSON
