# TaskMind AI - Testing Strategy

## Testing Pyramid /\

/E2\ 10% - End-to-End (critical paths only)
/\_**\_\
/ \
/ Integr \ 20% - Integration (API + DB)
/
/  
/ Unit Tests \ 70% - Unit (domain + use cases)
/\_\_\_\_**\

## Test Coverage Goals

| Layer                   | Target Coverage | Why?                                     |
| ----------------------- | --------------- | ---------------------------------------- |
| Domain                  | 100%            | Core business logic, must be bulletproof |
| Application (Use Cases) | 95%             | Orchestration logic, critical paths      |
| Infrastructure          | 70%             | External dependencies, harder to test    |
| Interface (API)         | 85%             | Public contracts, integration tests      |
| **Overall**             | **85%+**        | Industry standard for quality            |

---

## Unit Tests (70% of tests)

**What:** Test individual functions/classes in isolation
**Tools:** pytest, unittest.mock
**Speed:** <1 second for 100 tests

### Domain Layer Tests

````pythontests/unit/domain/entities/test_task.py
import pytest
from datetime import datetime
from apps.tasks.domain.entities import Task
from apps.tasks.domain.value_objects import Priorityclass TestTaskEntity:
"""Test Task domain entity"""def test_task_creation_defaults(self):
    """Task should have sensible defaults"""
    task = Task(title="Test", description="Test desc")    assert task.id is not None
    assert task.priority == Priority.MEDIUM
    assert task.urgency_score == 0.5
    assert task.ai_keywords == []
    assert isinstance(task.created_at, datetime)def test_mark_as_high_priority_when_urgent(self):
    """High urgency score should set priority to HIGH"""
    task = Task(title="Urgent", description="Server down")
    task.urgency_score = 0.85    task.mark_as_high_priority()    assert task.priority == Priority.HIGHdef test_is_urgent_threshold(self):
    """is_urgent() should return True when score > 0.7"""
    task = Task(title="Test", description="Test")    task.urgency_score = 0.6
    assert not task.is_urgent()    task.urgency_score = 0.8
    assert task.is_urgent()@pytest.mark.parametrize("score,expected_priority", [
    (0.2, Priority.LOW),
    (0.5, Priority.MEDIUM),
    (0.8, Priority.HIGH),
    (0.95, Priority.CRITICAL),
])
def test_priority_calculation(self, score, expected_priority):
    """Test priority calculation for different scores"""
    task = Task(title="Test", description="Test")
    task.urgency_score = score
    task.calculate_priority()    assert task.priority == expected_priority

### Application Layer Tests (Use Cases)
```pythontests/unit/application/use_cases/test_create_task.py
from unittest.mock import Mock, patch
import pytest
from apps.tasks.application.use_cases import CreateTaskUseCase, CreateTaskCommand
from apps.tasks.domain.entities import Task, Analysis
from apps.tasks.domain.repositories import TaskRepository
from apps.tasks.application.ports import AIServiceclass TestCreateTaskUseCase:
"""Test CreateTask use case with mocked dependencies"""@pytest.fixture
def mock_repository(self):
    """Mock task repository"""
    repo = Mock(spec=TaskRepository)
    repo.save.return_value = Task(
        title="Test",
        description="Test"
    )
    return repo@pytest.fixture
def mock_ai_service(self):
    """Mock AI service"""
    service = Mock(spec=AIService)
    service.analyze_urgency.return_value = Analysis(
        urgency_score=0.7,
        keywords=["test", "important"],
        confidence=0.9
    )
    return servicedef test_execute_creates_task_with_ai_analysis(
    self,
    mock_repository,
    mock_ai_service
):
    """Should create task with AI-analyzed urgency"""
    # Arrange
    use_case = CreateTaskUseCase(
        task_repository=mock_repository,
        ai_service=mock_ai_service
    )
    command = CreateTaskCommand(
        title="Important task",
        description="This needs attention"
    )    # Act
    result = use_case.execute(command)    # Assert
    assert result.urgency_score == 0.7
    assert "important" in result.ai_keywords
    mock_ai_service.analyze_urgency.assert_called_once()
    mock_repository.save.assert_called_once()def test_execute_handles_ai_service_failure(
    self,
    mock_repository,
    mock_ai_service
):
    """Should fallback gracefully if AI fails"""
    # Arrange
    mock_ai_service.analyze_urgency.side_effect = Exception("API down")
    use_case = CreateTaskUseCase(
        task_repository=mock_repository,
        ai_service=mock_ai_service
    )
    command = CreateTaskCommand(title="Test", description="Test")    # Act
    result = use_case.execute(command)    # Assert - should still create task with default values
    assert result is not None
    assert result.urgency_score == 0.5  # default fallback

---

## Integration Tests (20% of tests)

**What:** Test multiple components together (API + DB)
**Tools:** pytest-django, DRF test client
**Speed:** 5-10 seconds
```pythontests/integration/api/test_task_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.tasks.infrastructure.django_orm.models import TaskModelclass TaskAPITestCase(APITestCase):
"""Integration tests for Task API endpoints"""def setUp(self):
    """Setup test database"""
    self.list_url = reverse('task-list')
    self.task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }def test_create_task_returns_201(self):
    """POST /api/tasks/ should create task and return 201"""
    response = self.client.post(
        self.list_url,
        self.task_data,
        format='json'
    )    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == "Test Task"
    assert 'urgency_score' in response.data
    assert 'ai_keywords' in response.data    # Verify in database
    assert TaskModel.objects.count() == 1
    task = TaskModel.objects.first()
    assert task.title == "Test Task"def test_list_tasks_returns_paginated_results(self):
    """GET /api/tasks/ should return paginated tasks"""
    # Create test data
    TaskModel.objects.bulk_create([
        TaskModel(title=f"Task {i}", description="Test")
        for i in range(25)
    ])    response = self.client.get(self.list_url)    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert 'count' in response.data
    assert len(response.data['results']) == 20  # default page sizedef test_prioritized_endpoint_sorts_by_urgency(self):
    """GET /api/tasks/prioritized/ should sort by urgency_score DESC"""
    # Create tasks with different urgency
    TaskModel.objects.create(
        title="Low priority",
        urgency_score=0.2
    )
    TaskModel.objects.create(
        title="High priority",
        urgency_score=0.9
    )    url = reverse('task-prioritized')
    response = self.client.get(url)    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['title'] == "High priority"
    assert response.data[1]['title'] == "Low priority"def test_create_with_urgent_keywords_sets_high_priority(self):
    """Task with urgent keywords should get HIGH priority"""
    urgent_data = {
        "title": "CRITICAL BUG",
        "description": "Production server is down! Urgent fix needed."
    }    response = self.client.post(
        self.list_url,
        urgent_data,
        format='json'
    )    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['urgency_score'] > 0.7
    assert response.data['priority'] in ['HIGH', 'CRITICAL']

---

## E2E Tests (10% of tests)

**What:** Test complete user flows
**Tools:** Selenium (optional), API client
**Speed:** Slowest, run in CI only
```pythontests/e2e/test_task_workflow.py
import pytest
from rest_framework.test import APIClient@pytest.mark.e2e
class TestCompleteTaskWorkflow:
"""Test complete user journey"""def test_complete_task_lifecycle(self):
    """Create → Read → Update → Delete flow"""
    client = APIClient()    # 1. Create task
    create_response = client.post('/api/tasks/', {
        "title": "Implement feature X",
        "description": "Add new authentication system"
    })
    assert create_response.status_code == 201
    task_id = create_response.data['id']    # 2. Verify task appears in list
    list_response = client.get('/api/tasks/')
    assert any(t['id'] == task_id for t in list_response.data['results'])    # 3. Update task
    update_response = client.patch(f'/api/tasks/{task_id}/', {
        "status": "IN_PROGRESS"
    })
    assert update_response.data['status'] == "IN_PROGRESS"    # 4. Complete task
    complete_response = client.patch(f'/api/tasks/{task_id}/', {
        "status": "DONE"
    })
    assert complete_response.data['status'] == "DONE"    # 5. Delete task
    delete_response = client.delete(f'/api/tasks/{task_id}/')
    assert delete_response.status_code == 204    # 6. Verify deletion
    get_response = client.get(f'/api/tasks/{task_id}/')
    assert get_response.status_code == 404

---

## Test Configuration

### pytest.ini
```ini[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = test_.py
python_classes = Test
python_functions = test_*
addopts =
--verbose
--strict-markers
--cov=apps
--cov-report=html
--cov-report=term-missing
--cov-fail-under=85
markers =
unit: Unit tests (fast, isolated)
integration: Integration tests (DB required)
e2e: End-to-end tests (slow)
ai: Tests that use AI models (can be slow)

### conftest.py (shared fixtures)
```pythontests/conftest.py
import pytest
from unittest.mock import Mock
from apps.tasks.domain.repositories import TaskRepository
from apps.tasks.application.ports import AIService@pytest.fixture
def mock_task_repository():
"""Shared mock repository"""
return Mock(spec=TaskRepository)@pytest.fixture
def mock_ai_service():
"""Shared mock AI service"""
service = Mock(spec=AIService)
service.analyze_urgency.return_value = Analysis(
urgency_score=0.5,
keywords=[],
confidence=0.8
)
return service@pytest.fixture(scope='session')
def django_db_setup():
"""Use test database"""
pass

---

## Running Tests

### Local Development
```bashRun all tests
pytestRun only unit tests (fast)
pytest -m unitRun with coverage
pytest --cov=apps --cov-report=htmlRun specific test file
pytest tests/unit/domain/test_task.pyRun with verbose output
pytest -vvRun failed tests only
pytest --lfRun in parallel (faster)
pytest -n auto

### CI Pipeline
```bashIn GitHub Actions
pytest --cov=apps --cov-report=xml --junit-xml=junit.xml

---

## Code Coverage Reports

### Terminal Output----------- coverage: platform linux, python 3.11 -----------
Name                                     Stmts   Miss  Cover
apps/tasks/domain/entities/task.py          45      0   100%
apps/tasks/domain/services.py               30      2    93%
apps/tasks/application/use_cases.py         60      5    92%
apps/tasks/infrastructure/django_orm.py     40      8    80%
apps/tasks/interfaces/api/views.py          50     10    80%
TOTAL                                       225     25    89%

### HTML Report
```bashGenerate HTML coverage report
pytest --cov=apps --cov-report=htmlOpen in browser
open htmlcov/index.html

---

## TDD Workflow (Recommended)
Write failing test (RED)
↓
Write minimal code to pass (GREEN)
↓
Refactor while keeping tests green (REFACTOR)
↓
Repeat


**Example:**
```python1. RED - Write test first
def test_task_must_have_title():
with pytest.raises(ValueError):
Task(title="", description="Test")2. GREEN - Make it pass
class Task:
def init(self, title, description):
if not title:
raise ValueError("Title is required")
self.title = title3. REFACTOR - Improve without breaking
class Task:
def init(self, title, description):
self._validate_title(title)
self.title = titledef _validate_title(self, title):
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

---

## Test Data Factories (Optional but recommended)
```pythontests/factories.py
from factory.django import DjangoModelFactory
from apps.tasks.infrastructure.django_orm.models import TaskModelclass TaskFactory(DjangoModelFactory):
class Meta:
model = TaskModeltitle = factory.Faker('sentence', nb_words=4)
description = factory.Faker('paragraph')
priority = factory.Iterator(['LOW', 'MEDIUM', 'HIGH'])
urgency_score = factory.Faker('pyfloat', min_value=0, max_value=1)Usage in tests
def test_something():
task = TaskFactory.create(urgency_score=0.9)
assert task.urgency_score == 0.9

---

## Performance Testing (Bonus)
```pythontests/performance/test_api_performance.py
import pytest
from django.test.utils import override_settings@pytest.mark.performance
def test_list_tasks_performance(client, django_assert_num_queries):
"""List endpoint should not have N+1 queries"""
# Create test data
TaskFactory.create_batch(100)# Should use only 2 queries (count + select)
with django_assert_num_queries(2):
    response = client.get('/api/tasks/')
    assert response.status_code == 200

---

## What to Show in Interview

1. **Run full test suite:**
```bashpytest -v
Show all green checkmarks

2. **Show coverage report:**
```bashpytest --cov=apps --cov-report=term-missing
Point out >85% coverage

3. **Explain testing pyramid:**
   "70% unit tests because they're fast and test core logic in isolation"

4. **Show example of mocking:**
   "Here I mock the AI service so tests don't depend on external APIs"

5. **Show TDD example:**
   "I write tests first to drive design - this test forced me to add validation"

---

## Anti-Patterns to Avoid

❌ **Don't:**
- Test Django framework itself (don't test `.save()` works)
- Write integration tests for everything (too slow)
- Mock everything (integration tests need real DB)
- Skip edge cases
- Have tests depend on each other

✅ **Do:**
- Test your business logic thoroughly
- Balance unit/integration/e2e
- Mock external dependencies (AI APIs, email)
- Test error paths
- Keep tests isolated
````
