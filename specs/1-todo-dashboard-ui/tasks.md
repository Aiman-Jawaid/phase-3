---
description: "Task list for Todo Dashboard UI implementation"
---

# Tasks: Todo Dashboard UI

**Input**: Design documents from `/specs/1-todo-dashboard-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as specified in the feature requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` for the Next.js application
- Paths shown below follow the plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create frontend project structure per implementation plan
- [X] T002 Initialize Next.js 16+ project with TypeScript and Tailwind CSS dependencies
- [X] T003 [P] Configure linting and formatting tools (ESLint, Prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Configure Tailwind CSS with specified color palette (light gray #F9FAFB, indigo/blue)
- [X] T005 [P] Create shared UI components directory structure in frontend/components/ui/
- [X] T006 [P] Set up API client in frontend/lib/api.ts for JWT-secured API calls
- [X] T007 Create TypeScript types in frontend/lib/types.ts for Task and User entities
- [X] T008 Configure Next.js App Router with proper layout structure
- [X] T009 Set up responsive design foundation for desktop and tablet

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement core dashboard functionality allowing users to view and manage their tasks with clear visual indicators

**Independent Test**: Can be fully tested by visiting the dashboard page and verifying that tasks are displayed in a clean, organized manner with clear visual indicators for completion status.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Component test for TasksArea in frontend/tests/components/TasksArea.test.tsx
- [X] T011 [P] [US1] Component test for Header in frontend/tests/components/Header.test.tsx

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Header component in frontend/components/Header.tsx
- [X] T013 [P] [US1] Create PageTitleSection component in frontend/components/PageTitleSection.tsx
- [X] T014 [US1] Implement TasksArea component in frontend/components/TasksArea.tsx
- [X] T015 [US1] Create task card UI with completion status indicators in frontend/components/TasksArea.tsx
- [X] T016 [US1] Implement task listing functionality in frontend/app/page.tsx
- [X] T017 [US1] Add styling following specified color scheme and layout requirements

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Track Daily Progress (Priority: P2)

**Goal**: Implement progress card showing daily progress and completed task statistics to motivate users

**Independent Test**: Can be fully tested by viewing the progress card on the dashboard and verifying that it displays accurate completion statistics.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T018 [P] [US2] Component test for ProgressCard in frontend/tests/components/ProgressCard.test.tsx

### Implementation for User Story 2

- [X] T019 [P] [US2] Create ProgressCard component in frontend/components/ProgressCard.tsx
- [X] T020 [US2] Implement progress calculation logic for completed vs total tasks
- [X] T021 [US2] Add progress visualization with indigo gradient background
- [X] T022 [US2] Integrate ProgressCard with User Story 1 components in frontend/app/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Experience Empty State (Priority: P3)

**Goal**: Implement friendly empty state for new users with no tasks, including clear instructions

**Independent Test**: Can be fully tested by viewing the dashboard when no tasks exist and verifying that a friendly empty state is displayed with clear instructions.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US3] Component test for EmptyState in frontend/tests/components/EmptyState.test.tsx

### Implementation for User Story 3

- [X] T024 [P] [US3] Create EmptyState component in frontend/components/EmptyState.tsx
- [X] T025 [US3] Implement conditional rendering between tasks and empty state in TasksArea
- [X] T026 [US3] Add "No todos yet" text and Add Task button to EmptyState component
- [X] T027 [US3] Add icon to EmptyState component and ensure proper styling

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T028 [P] Documentation updates in frontend/README.md
- [X] T029 Code cleanup and refactoring across all components
- [X] T030 [P] Additional component tests in frontend/tests/components/
- [X] T031 Security hardening - ensure proper JWT handling in API calls
- [X] T032 Run quickstart.md validation to ensure all functionality works
- [X] T033 Final responsive testing on desktop and tablet devices

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Component test for TasksArea in frontend/tests/components/TasksArea.test.tsx"
Task: "Component test for Header in frontend/tests/components/Header.test.tsx"

# Launch all components for User Story 1 together:
Task: "Create Header component in frontend/components/Header.tsx"
Task: "Create PageTitleSection component in frontend/components/PageTitleSection.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence