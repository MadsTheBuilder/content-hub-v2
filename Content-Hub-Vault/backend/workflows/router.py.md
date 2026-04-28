---
status: Synced
last_sync: "2026-04-09 23:47"
original_path: "backend/workflows/router.py"
---
# router.py

## Python Structure Summary

```python
def get_templates():
def list_workflows(user=Depends(get_current_user)):
def create_workflow_endpoint(data: WorkflowCreate, user=Depends(get_current_user)):
def get_workflow(workflow_id: str, user=Depends(get_current_user)):
def update_workflow(workflow_id: str, data: WorkflowUpdate, user=Depends(get_current_user)):
def delete_workflow(workflow_id: str, user=Depends(get_current_user)):
def trigger_scrape(workflow_id: str, user=Depends(get_current_user)):
def get_trending(workflow_id: str, user=Depends(get_current_user)):
def get_suggestions(workflow_id: str, user=Depends(get_current_user)):
class SelectionRecord:
def record_selections(workflow_id: str, data: SelectionRecord, user=Depends(get_current_user)):
```
