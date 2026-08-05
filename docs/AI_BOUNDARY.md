# AI Boundary

AI is used only after deterministic evidence reconstruction.

## Allowed

- summarize selected evidence
- extract structured fields from technician notes
- draft suggested next action
- explain missing evidence
- cite source events included in the pack

## Not Allowed

- read raw customer systems directly
- invent evidence
- infer causality as fact
- trigger deployment, rollback, dispatch or machine control
- override human decision owners

## Prompt Contract

Input:

- decision under review
- normalized events
- relationships
- missing evidence
- prior cases

Output:

```json
{
  "summary": "string",
  "suggested_next_action": "string",
  "uncertainties": ["string"],
  "citations": ["event_id"]
}
```

If the evidence is insufficient, the model must say what is missing.

