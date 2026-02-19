# Task Manager - Module Dependencies & Conflict Points

## Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────┐
│                      main.py (Example App)                   │
│              (Uses all other modules for demo)               │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   ┌─────────┐      ┌──────────┐      ┌──────────┐
   │manager  │      │database  │      │  config  │
   │  .py    │      │   .py    │      │   .py    │
   └────┬────┘      └─────┬────┘      └──────────┘
        │                 │
        └────────┬────────┘
                 │
                 ▼
           ┌──────────┐
           │ models   │
           │   .py    │
           └──────────┘
                 │
                 ├─────────────────┐
                 │                 │
                 ▼                 ▼
          ┌──────────┐      ┌──────────┐
          │ utils    │      │__init__  │
          │  .py     │      │   .py    │
          └──────────┘      └──────────┘

           ┌──────────┐
           │test_     │ (Tests all modules)
           │manager.py│
           └──────────┘
```

## Key Dependencies

### main.py → All modules
- Imports: TaskManager, Database, TaskPriority
- Uses: config, models, database, manager
- Type: Orchestration (imports and demonstrates everything)

### manager.py → models.py, database.py
- Imports: Task, Project, TaskStatus, TaskPriority, Database
- Type: Business logic layer (orchestrates data operations)

### database.py → models.py
- Imports: Task, Project, TaskStatus, TaskPriority
- Type: Persistence layer (serializes and deserializes models)

### models.py → (No internal dependencies)
- Imports: enum, datetime, typing
- Type: Core domain models (pure data classes)

### config.py → (No internal dependencies)
- Imports: os, typing
- Type: Configuration management

### utils.py → (No internal dependencies)
- Imports: datetime, typing, re
- Type: Utility functions (stateless helper functions)

### __init__.py → models.py, database.py, manager.py
- Exports: Task, Project, Database, TaskManager
- Type: Package interface

### test_manager.py → All modules
- Imports: All models, database, manager, utils
- Type: Comprehensive test suite

## Potential Conflict Scenarios

### Scenario 1: Model Changes
**File**: models.py
**Impact**:
- database.py (serialization logic in to_dict())
- manager.py (uses Task/Project properties)
- test_manager.py (model tests need updates)

**Example Conflict**: Adding a new field to Task model
```python
# Colleague 1: Adds 'tags' field
self.tags: List[str] = []

# Colleague 2: Adds 'attachments' field
self.attachments: List[str] = []

# Conflict in: __init__, to_dict(), test cases
```

### Scenario 2: Database Interface Changes
**File**: database.py
**Impact**:
- manager.py (calls database methods)
- main.py (creates Database instance)
- test_manager.py (database tests)

**Example Conflict**: Changing method signatures
```python
# Colleague 1: Changes parameter order
def create_task(self, project_id, title, description, priority):

# Colleague 2: Changes parameter names
def create_task(self, name, desc, project_id, level):

# Conflict: All callers need updating
```

### Scenario 3: Manager API Changes
**File**: manager.py
**Impact**:
- main.py (all usage examples)
- test_manager.py (manager tests)

**Example Conflict**: Adding vs modifying methods
```python
# Colleague 1: Adds get_team_tasks(team_id)
def get_team_tasks(self, team_id: int) -> List[Task]:

# Colleague 2: Modifies get_my_tasks() signature
def get_my_tasks(self, status: TaskStatus = None) -> List[Task]:

# Conflict: Different approach to same functionality
```

### Scenario 4: Cross-Module Refactoring
**Files**: models.py + database.py
**Impact**: Both files modified together

**Example Conflict**: Moving responsibility
```python
# Colleague 1: Moves get_completion_rate() from Project to Database
# Colleague 2: Adds new method get_project_health() to Project

# Conflict: Both modifying class structure simultaneously
```

### Scenario 5: Multiple Imports in main.py
**File**: main.py
**Impact**: Imports from multiple modules

**Example Conflict**: Different feature implementations
```python
# Colleague 1: Adds notification system
from task_manager.notifications import Notifier

# Colleague 2: Adds reporting system
from task_manager.reports import Reporter

# Conflict: Both adding imports and features
```

## Best Practices for Conflict Resolution

### 1. **Understand Dependencies First**
   - Know which files depend on the one you're modifying
   - Check all imports of changed classes/functions

### 2. **Prioritize Core Models**
   - models.py is the foundation
   - Changes here cascade to other files
   - Resolve model conflicts first

### 3. **Test After Resolution**
   - Run test_manager.py to verify consistency
   - All 22 tests should pass after conflict resolution

### 4. **Review Method Signatures**
   - If signature changes, update all callers
   - Check main.py and test files for usage

### 5. **Maintain Semantic Consistency**
   - Ensure business logic remains intact
   - Data flow should be preserved

## Files by Complexity

### Simple (No/Few Dependencies)
- utils.py - Pure utility functions
- config.py - Configuration only
- models.py - Data classes (no internal dependencies)

### Medium (Some Dependencies)
- database.py - Depends on models.py
- manager.py - Depends on models.py, database.py

### Complex (Multiple Dependencies)
- main.py - Uses all modules
- test_manager.py - Tests all modules
- __init__.py - Re-exports from all modules

## Testing Conflicts

After resolving conflicts, verify:
```bash
# Run all tests
python -m unittest task_manager/test_manager.py -v

# Check imports work
python -c "from task_manager import TaskManager, Database, Task, Project"

# Run example
python task_manager/main.py
```

---

This structure ensures that learning conflict resolution is realistic and comprehensive!

