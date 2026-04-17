import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

DEMO_BOARD_ID = "demo-board"
DEMO_BOARDS: List[Dict[str, Any]] = [
    {
        "id": DEMO_BOARD_ID,
        "name": "Getting Started Board",
        "description": "Supabase schema is not set up yet. Run supabase_schema.sql to switch to live data.",
        "owner": "Demo Mode",
        "is_demo": True,
    }
]
DEMO_RESOURCES: List[Dict[str, Any]] = [
    {
        "id": "demo-resource-1",
        "board_id": DEMO_BOARD_ID,
        "title": "Initialize Supabase Schema",
        "description": "Open Supabase SQL Editor and execute supabase_schema.sql from this project.",
        "url": "https://supabase.com/dashboard/project/_/sql/new",
        "type": "link",
        "tags": "Setup, Supabase, Getting Started",
        "storage_path": None,
    },
    {
        "id": "demo-resource-2",
        "board_id": DEMO_BOARD_ID,
        "title": "Run Local App",
        "description": "Start the server locally with: uv run uvicorn app:app --reload",
        "url": "http://localhost:8000",
        "type": "link",
        "tags": "Local Dev, Runbook",
        "storage_path": None,
    },
]
_MISSING_SCHEMA_NOTICE_SHOWN = False


EXAMPLE_BOARDS: List[Dict[str, Any]] = [
    {
        "name": "Assignment Board - Sem VI",
        "description": "Assignment tracker for Semester VI across SPCC, MC, CSS, QA, and Cloud Computing.",
        "resources": [
            {
                "title": "SPCC Assignment 1",
                "description": "System Programming and Compiler Construction assignment set 1.",
                "url": "https://example.com/assignments/sem6/spcc/1",
                "type": "link",
                "tags": "Sem VI, SPCC, Assignment 1",
            },
            {
                "title": "SPCC Assignment 2",
                "description": "System Programming and Compiler Construction assignment set 2.",
                "url": "https://example.com/assignments/sem6/spcc/2",
                "type": "link",
                "tags": "Sem VI, SPCC, Assignment 2",
            },
            {
                "title": "MC Assignment 1",
                "description": "Mobile Computing assignment set 1.",
                "url": "https://example.com/assignments/sem6/mc/1",
                "type": "link",
                "tags": "Sem VI, MC, Assignment 1",
            },
            {
                "title": "MC Assignment 2",
                "description": "Mobile Computing assignment set 2.",
                "url": "https://example.com/assignments/sem6/mc/2",
                "type": "link",
                "tags": "Sem VI, MC, Assignment 2",
            },
            {
                "title": "CSS Assignment 1",
                "description": "Cryptography and System Security assignment set 1.",
                "url": "https://example.com/assignments/sem6/css/1",
                "type": "link",
                "tags": "Sem VI, CSS, Assignment 1",
            },
            {
                "title": "CSS Assignment 2",
                "description": "Cryptography and System Security assignment set 2.",
                "url": "https://example.com/assignments/sem6/css/2",
                "type": "link",
                "tags": "Sem VI, CSS, Assignment 2",
            },
            {
                "title": "QA Assignment 1",
                "description": "Quantitative Analysis assignment set 1.",
                "url": "https://example.com/assignments/sem6/qa/1",
                "type": "link",
                "tags": "Sem VI, QA, Assignment 1",
            },
            {
                "title": "QA Assignment 2",
                "description": "Quantitative Analysis assignment set 2.",
                "url": "https://example.com/assignments/sem6/qa/2",
                "type": "link",
                "tags": "Sem VI, QA, Assignment 2",
            },
            {
                "title": "Cloud Computing Assignment 1",
                "description": "Cloud Computing assignment set 1.",
                "url": "https://example.com/assignments/sem6/cloud/1",
                "type": "link",
                "tags": "Sem VI, Cloud Computing, Assignment 1",
            },
            {
                "title": "Cloud Computing Assignment 2",
                "description": "Cloud Computing assignment set 2.",
                "url": "https://example.com/assignments/sem6/cloud/2",
                "type": "link",
                "tags": "Sem VI, Cloud Computing, Assignment 2",
            },
        ],
    },
    {
        "name": "Experiment Board - Cloud Computing",
        "description": "Cloud Computing Lab experiment index with direct links to experiment notes.",
        "resources": [
            {
                "title": "Experiment 1 - Intro to Cloud Computing",
                "description": "Overview of cloud service models and deployment models.",
                "url": "https://example.com/cloud-lab/experiments/1",
                "type": "link",
                "tags": "Cloud Computing, Experiment, Semester VI",
            },
            {
                "title": "Experiment 2 - Hosted Virtualization with VirtualBox",
                "description": "Install and configure hosted virtualization.",
                "url": "https://example.com/cloud-lab/experiments/2",
                "type": "link",
                "tags": "Cloud Computing, Virtualization, Experiment",
            },
            {
                "title": "Experiment 3 - Bare-Metal Virtualization",
                "description": "Study Xen/HyperV/VMware ESXi setup and architecture.",
                "url": "https://example.com/cloud-lab/experiments/3",
                "type": "link",
                "tags": "Cloud Computing, Bare Metal, Experiment",
            },
            {
                "title": "Experiment 4 - IaaS on AWS or Azure",
                "description": "Provision and monitor infrastructure resources in cloud.",
                "url": "https://example.com/cloud-lab/experiments/4",
                "type": "link",
                "tags": "Cloud Computing, IaaS, Experiment",
            },
            {
                "title": "Experiment 5 - PaaS Deployment",
                "description": "Deploy an app using Elastic Beanstalk or Azure App Service.",
                "url": "https://example.com/cloud-lab/experiments/5",
                "type": "link",
                "tags": "Cloud Computing, PaaS, Experiment",
            },
            {
                "title": "Experiment 6 - Storage as a Service",
                "description": "Use S3/Glacier/Azure Storage for object lifecycle.",
                "url": "https://example.com/cloud-lab/experiments/6",
                "type": "link",
                "tags": "Cloud Computing, Storage, Experiment",
            },
            {
                "title": "Experiment 7 - DBaaS SQL and NoSQL",
                "description": "Configure and compare managed SQL and NoSQL services.",
                "url": "https://example.com/cloud-lab/experiments/7",
                "type": "link",
                "tags": "Cloud Computing, DBaaS, Experiment",
            },
            {
                "title": "Experiment 8 - Security as a Service",
                "description": "Configure cloud security controls and monitoring.",
                "url": "https://example.com/cloud-lab/experiments/8",
                "type": "link",
                "tags": "Cloud Computing, Security, Experiment",
            },
            {
                "title": "Experiment 9 - IAM Practices",
                "description": "Implement least privilege and role-based access workflows.",
                "url": "https://example.com/cloud-lab/experiments/9",
                "type": "link",
                "tags": "Cloud Computing, IAM, Experiment",
            },
            {
                "title": "Experiment 10 - Containerization with Docker",
                "description": "Build, run, and publish cloud-ready Docker images.",
                "url": "https://example.com/cloud-lab/experiments/10",
                "type": "link",
                "tags": "Cloud Computing, Docker, Experiment",
            },
        ],
    },
    {
        "name": "Notice Board - Department Updates",
        "description": "Department notices for holidays, exams, attendance, and administrative updates.",
        "resources": [
            {
                "title": "Holiday Notice - Ram Navami",
                "description": "Campus holiday declaration and class rescheduling details.",
                "url": "https://example.com/notices/holiday-ram-navami",
                "type": "link",
                "tags": "Notice, Holiday, Department",
            },
            {
                "title": "Mid-Sem Exam Timetable",
                "description": "Official exam schedule for Semester VI.",
                "url": "https://example.com/notices/midsem-timetable",
                "type": "link",
                "tags": "Notice, Exam, Sem VI",
            },
            {
                "title": "Defaulter List - Attendance",
                "description": "Students below attendance threshold with action steps.",
                "url": "https://example.com/notices/defaulter-attendance",
                "type": "link",
                "tags": "Notice, Defaulter, Attendance",
            },
            {
                "title": "End-Sem Practical Exam Circular",
                "description": "Lab practical slots, batch timing, and instructions.",
                "url": "https://example.com/notices/practical-exam-circular",
                "type": "link",
                "tags": "Notice, Practical, Exam",
            },
            {
                "title": "Fee Payment Reminder",
                "description": "Last date reminder for pending semester fee submission.",
                "url": "https://example.com/notices/fee-reminder",
                "type": "link",
                "tags": "Notice, Fees, Administration",
            },
            {
                "title": "Project Review Meeting",
                "description": "Project review calendar and reporting format update.",
                "url": "https://example.com/notices/project-review",
                "type": "link",
                "tags": "Notice, Project, Academic",
            },
        ],
    },
]


def _is_schema_missing_error(error: Exception) -> bool:
    message = str(error)
    return "PGRST205" in message or "Could not find the table 'public." in message


def _is_permission_error(error: Exception) -> bool:
    message = str(error).lower()
    return "permission denied" in message or "row-level security" in message or "jwt" in message


def _is_missing_column_error(error: Exception, column_name: str) -> bool:
    message = str(error).lower()
    return column_name.lower() in message and "column" in message


def _normalize_tags(tags: Optional[str]) -> Optional[str]:
    if not tags:
        return None
    items = [item.strip() for item in tags.split(",") if item.strip()]
    if not items:
        return None
    return ", ".join(items)


def _append_tags_to_description(description: Optional[str], tags: Optional[str]) -> Optional[str]:
    normalized_tags = _normalize_tags(tags)
    base_description = (description or "").strip()
    if not normalized_tags:
        return base_description or None
    if "Tags:" in base_description:
        return base_description
    if base_description:
        return f"{base_description} | Tags: {normalized_tags}"
    return f"Tags: {normalized_tags}"


def _insert_resource_with_column_fallback(client: Client, payload: Dict[str, Any]):
    working_payload = dict(payload)
    for _ in range(3):
        try:
            return client.table("resources").insert(working_payload).execute()
        except Exception as insert_error:
            removed_any = False
            for column in ("storage_path", "tags"):
                if column in working_payload and _is_missing_column_error(insert_error, column):
                    if column == "tags":
                        working_payload["description"] = _append_tags_to_description(
                            working_payload.get("description"),
                            working_payload.get("tags"),
                        )
                    working_payload.pop(column, None)
                    removed_any = True
            if removed_any:
                continue
            raise
    return client.table("resources").insert(working_payload).execute()


def _update_resource_with_column_fallback(client: Client, resource_id: str, payload: Dict[str, Any]):
    working_payload = dict(payload)
    for _ in range(3):
        try:
            return client.table("resources").update(working_payload).eq("id", resource_id).execute()
        except Exception as update_error:
            removed_any = False
            for column in ("storage_path", "tags"):
                if column in working_payload and _is_missing_column_error(update_error, column):
                    if column == "tags":
                        working_payload["description"] = _append_tags_to_description(
                            working_payload.get("description"),
                            working_payload.get("tags"),
                        )
                    working_payload.pop(column, None)
                    removed_any = True
            if removed_any:
                continue
            raise
    return client.table("resources").update(working_payload).eq("id", resource_id).execute()


def _warn_missing_schema_once() -> None:
    global _MISSING_SCHEMA_NOTICE_SHOWN
    if _MISSING_SCHEMA_NOTICE_SHOWN:
        return
    print("Database schema missing. Apply supabase_schema.sql in Supabase SQL editor.")
    _MISSING_SCHEMA_NOTICE_SHOWN = True


def _get_demo_board_by_id(board_id: str) -> Optional[Dict[str, Any]]:
    for board in DEMO_BOARDS:
        if board["id"] == board_id:
            return board
    return None


def _get_demo_resource_by_id(resource_id: str) -> Optional[Dict[str, Any]]:
    for resource in DEMO_RESOURCES:
        if resource["id"] == resource_id:
            return resource
    return None

def get_client(access_token: Optional[str] = None) -> Client:
    """Returns a Supabase client configured with the user's access token if provided."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    if access_token:
        client.postgrest.auth(access_token)
        # PostgREST auth header is enough for RLS-aware DB queries.
        # Avoid set_session() here because we do not have a refresh token,
        # and passing an empty one can clear auth context.
    return client


def get_service_client() -> Optional[Client]:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None

def get_all_boards(access_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all boards accessible to the current user."""
    client = get_client(access_token)
    try:
        response = client.table("boards").select("*").execute()
        boards = response.data
        for board in boards:
            # Mocking owner since we don't have a profiles table
            board["owner"] = "Team Member"
        return boards
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            return DEMO_BOARDS
        print(f"Database error (get_all_boards): {e}")
        return []

def get_board_by_id(board_id: str, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetches a specific board by ID."""
    client = get_client(access_token)
    try:
        response = client.table("boards").select("*").eq("id", board_id).single().execute()
        return response.data
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            return _get_demo_board_by_id(board_id)
        print(f"Database error (get_board_by_id): {e}")
        return None

def get_resources_by_board(
    board_id: str,
    access_token: Optional[str] = None,
    resource_type: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetches resources for a specific board."""
    client = get_client(access_token)
    try:
        query = client.table("resources").select("*").eq("board_id", board_id)
        if resource_type and resource_type in {"link", "file", "image", "video"}:
            query = query.eq("type", resource_type)
        if tag and tag.strip():
            query = query.ilike("tags", f"%{tag.strip()}%")
        response = query.execute()
        return response.data
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            resources = [item for item in DEMO_RESOURCES if item["board_id"] == board_id]
            if resource_type and resource_type in {"link", "file", "image", "video"}:
                resources = [item for item in resources if item.get("type") == resource_type]
            if tag and tag.strip():
                needle = tag.strip().lower()
                resources = [
                    item
                    for item in resources
                    if needle in (item.get("tags") or "").lower()
                ]
            return resources
        print(f"Database error (get_resources_by_board): {e}")
        return []


def get_resource_by_id(resource_id: str, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetches a specific resource by ID."""
    client = get_client(access_token)
    try:
        response = client.table("resources").select("*").eq("id", resource_id).single().execute()
        return response.data
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            return _get_demo_resource_by_id(resource_id)
        print(f"Database error (get_resource_by_id): {e}")
        return None


def _create_board_via_service_role(payload: Dict[str, Any], created_by: Optional[str]) -> Optional[Dict[str, Any]]:
    if not created_by:
        return None

    service_client = get_service_client()
    if not service_client:
        return None

    try:
        service_payload = dict(payload)
        service_payload["created_by"] = created_by
        response = service_client.table("boards").insert(service_payload).execute()
        rows = response.data or []
        if not rows:
            return None
        board = rows[0]
        board["owner"] = "Team Member"
        return board
    except Exception as service_error:
        print(f"Database error (create_board service fallback): {service_error}")
        return None


def create_board(
    name: str,
    description: str,
    access_token: Optional[str] = None,
    created_by: Optional[str] = None,
) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Creates a new board and returns (board, error_message)."""
    board_name = name.strip()
    if not board_name:
        return None, "Board name is required."

    payload = {
        "name": board_name,
        "description": description.strip() if description else None,
        "is_public": False,
    }
    client = get_client(access_token)

    try:
        response = client.table("boards").insert(payload).execute()
        rows = response.data or []
        if not rows:
            return None, "Board was not created. Please try again."
        board = rows[0]
        board["owner"] = "Team Member"
        return board, None
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            new_board = {
                "id": str(uuid4()),
                "name": board_name,
                "description": description.strip() if description else "No description yet.",
                "owner": "Demo Mode",
                "is_demo": True,
            }
            DEMO_BOARDS.insert(0, new_board)
            return new_board, None

        message = str(e)
        lower_message = message.lower()
        if "jwt" in lower_message or "row-level security" in lower_message or "permission denied" in lower_message:
            fallback_board = _create_board_via_service_role(payload, created_by)
            if fallback_board:
                return fallback_board, None
            return None, "Please sign in to create a board."

        print(f"Database error (create_board): {e}")
        return None, "Could not create board right now."


def set_board_visibility(
    board_id: str,
    is_public: bool,
    access_token: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """Updates board visibility and returns (success, error_message)."""
    client = get_client(access_token)
    try:
        response = client.table("boards").update({"is_public": is_public}).eq("id", board_id).execute()
        rows = response.data or []
        if not rows:
            return False, "Board not found."
        return True, None
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            board = _get_demo_board_by_id(board_id)
            if not board:
                return False, "Board not found."
            board["is_public"] = is_public
            return True, None
        if _is_permission_error(e):
            return False, "You are not allowed to change board sharing settings."
        print(f"Database error (set_board_visibility): {e}")
        return False, "Could not update board visibility right now."


def create_resource(
    board_id: str,
    title: str,
    description: str,
    url: Optional[str],
    resource_type: str,
    storage_path: Optional[str],
    tags: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Creates a resource and returns (resource, error_message)."""
    resource_title = title.strip()
    if not resource_title:
        return None, "Resource title is required."

    safe_type = resource_type if resource_type in {"link", "file", "image", "video"} else "link"
    payload: Dict[str, Any] = {
        "board_id": board_id,
        "title": resource_title,
        "description": description.strip() if description else None,
        "url": url.strip() if url else None,
        "type": safe_type,
        "tags": _normalize_tags(tags),
    }
    if storage_path:
        payload["storage_path"] = storage_path

    client = get_client(access_token)
    try:
        response = _insert_resource_with_column_fallback(client, payload)
        rows = response.data or []
        if not rows:
            return None, "Resource was not created. Please try again."
        return rows[0], None
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            new_resource = {
                "id": str(uuid4()),
                "board_id": board_id,
                "title": resource_title,
                "description": description.strip() if description else "",
                "url": url.strip() if url else None,
                "type": safe_type,
                "tags": _normalize_tags(tags),
                "storage_path": storage_path,
            }
            DEMO_RESOURCES.insert(0, new_resource)
            return new_resource, None

        if _is_permission_error(e):
            return None, "Please sign in and ensure you have access to this board."

        print(f"Database error (create_resource): {e}")
        return None, "Could not create resource right now."


def update_resource(
    resource_id: str,
    title: str,
    description: str,
    url: Optional[str],
    resource_type: str,
    storage_path: Optional[str],
    tags: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Updates a resource and returns (resource, error_message)."""
    resource_title = title.strip()
    if not resource_title:
        return None, "Resource title is required."

    safe_type = resource_type if resource_type in {"link", "file", "image", "video"} else "link"
    payload: Dict[str, Any] = {
        "title": resource_title,
        "description": description.strip() if description else None,
        "url": url.strip() if url else None,
        "type": safe_type,
        "tags": _normalize_tags(tags),
    }
    if storage_path is not None:
        payload["storage_path"] = storage_path

    client = get_client(access_token)
    try:
        response = _update_resource_with_column_fallback(client, resource_id, payload)
        rows = response.data or []
        if not rows:
            return None, "Resource not found."
        return rows[0], None
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            demo_resource = _get_demo_resource_by_id(resource_id)
            if not demo_resource:
                return None, "Resource not found."
            demo_resource["title"] = resource_title
            demo_resource["description"] = description.strip() if description else ""
            demo_resource["url"] = url.strip() if url else None
            demo_resource["type"] = safe_type
            demo_resource["tags"] = _normalize_tags(tags)
            if storage_path is not None:
                demo_resource["storage_path"] = storage_path
            return demo_resource, None

        if _is_permission_error(e):
            return None, "You are not allowed to update this resource."

        print(f"Database error (update_resource): {e}")
        return None, "Could not update resource right now."


def delete_resource(resource_id: str, access_token: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Deletes a resource and returns (deleted_resource, error_message)."""
    client = get_client(access_token)
    try:
        response = client.table("resources").delete().eq("id", resource_id).execute()
        rows = response.data or []
        if not rows:
            return None, "Resource not found."
        return rows[0], None
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            demo_resource = _get_demo_resource_by_id(resource_id)
            if not demo_resource:
                return None, "Resource not found."
            DEMO_RESOURCES.remove(demo_resource)
            return demo_resource, None

        if _is_permission_error(e):
            return None, "You are not allowed to delete this resource."

        print(f"Database error (delete_resource): {e}")
        return None, "Could not delete resource right now."


def seed_example_boards(access_token: Optional[str] = None) -> Tuple[int, int, Optional[str]]:
    """Creates Assignment, Experiment, and Notice example boards with seed resources."""
    if not access_token and SUPABASE_SERVICE_KEY:
        return _seed_example_boards_with_service_role()

    boards_created = 0
    resources_created = 0

    client = get_client(access_token)
    boards = get_all_boards(access_token)
    boards_by_name = {
        board.get("name", "").strip().lower(): board
        for board in boards
        if board.get("name")
    }

    for board_template in EXAMPLE_BOARDS:
        board_name = board_template["name"].strip()
        board_key = board_name.lower()
        board = boards_by_name.get(board_key)

        if not board:
            board, board_error = create_board(
                name=board_name,
                description=board_template.get("description", ""),
                access_token=access_token,
            )
            if board_error:
                return boards_created, resources_created, board_error
            if not board:
                return boards_created, resources_created, "Could not create example board right now."
            boards_created += 1
            boards_by_name[board_key] = board

        board_id = board.get("id")
        if not board_id:
            continue

        _, visibility_error = set_board_visibility(board_id, True, access_token)
        if visibility_error and visibility_error != "Board not found.":
            return boards_created, resources_created, visibility_error

        existing_resources = get_resources_by_board(board_id, access_token)
        existing_by_title = {
            item.get("title", "").strip().lower(): item
            for item in existing_resources
            if item.get("title")
        }
        existing_titles = set(existing_by_title.keys())

        for resource_template in board_template.get("resources", []):
            title = resource_template.get("title", "").strip()
            if not title:
                continue
            title_key = title.lower()
            if title_key in existing_titles:
                existing_resource = existing_by_title.get(title_key) or {}
                desired_tags = _normalize_tags(resource_template.get("tags"))
                if desired_tags and not _normalize_tags(existing_resource.get("tags")) and existing_resource.get("id"):
                    try:
                        _update_resource_with_column_fallback(
                            client,
                            existing_resource["id"],
                            {
                                "description": _append_tags_to_description(
                                    existing_resource.get("description"),
                                    desired_tags,
                                ),
                                "tags": desired_tags,
                            },
                        )
                    except Exception as e:
                        if _is_permission_error(e):
                            return boards_created, resources_created, "Please sign in and ensure you have access to update example resources."
                        print(f"Database error (seed tag backfill): {e}")
                        return boards_created, resources_created, "Could not update tags for existing example resources."
                continue

            _, resource_error = create_resource(
                board_id=board_id,
                title=title,
                description=resource_template.get("description", ""),
                url=resource_template.get("url"),
                resource_type=resource_template.get("type", "link"),
                storage_path=None,
                tags=resource_template.get("tags"),
                access_token=access_token,
            )
            if resource_error:
                return boards_created, resources_created, resource_error

            existing_titles.add(title_key)
            resources_created += 1

    return boards_created, resources_created, None


def _seed_example_boards_with_service_role() -> Tuple[int, int, Optional[str]]:
    """Seeds example boards/resources using service role to bypass RLS for setup workflows."""
    client = get_service_client()
    if not client:
        return 0, 0, "Service key is not configured for example seeding."

    boards_created = 0
    resources_created = 0

    try:
        board_rows = client.table("boards").select("id,name,is_public").execute().data or []
    except Exception as e:
        if _is_schema_missing_error(e):
            _warn_missing_schema_once()
            board_rows = DEMO_BOARDS
        else:
            print(f"Database error (seed boards fetch): {e}")
            return 0, 0, "Could not load existing boards for seeding."

    boards_by_name = {
        row.get("name", "").strip().lower(): row
        for row in board_rows
        if row.get("name")
    }

    for board_template in EXAMPLE_BOARDS:
        board_name = board_template["name"].strip()
        board_key = board_name.lower()
        board_row = boards_by_name.get(board_key)

        if not board_row:
            try:
                inserted = client.table("boards").insert(
                    {
                        "name": board_name,
                        "description": board_template.get("description", ""),
                        "is_public": True,
                    }
                ).execute().data or []
            except Exception as e:
                print(f"Database error (seed board insert): {e}")
                return boards_created, resources_created, "Could not create an example board right now."

            if not inserted:
                return boards_created, resources_created, "Could not create an example board right now."

            board_row = inserted[0]
            boards_by_name[board_key] = board_row
            boards_created += 1

        board_id = board_row.get("id")
        if not board_id:
            continue

        if not board_row.get("is_public"):
            try:
                client.table("boards").update({"is_public": True}).eq("id", board_id).execute()
                board_row["is_public"] = True
            except Exception as e:
                print(f"Database error (seed board visibility): {e}")
                return boards_created, resources_created, "Could not make example board shareable right now."

        try:
            existing_resources = client.table("resources").select("id,title,description,tags").eq("board_id", board_id).execute().data or []
        except Exception as e:
            if _is_schema_missing_error(e):
                _warn_missing_schema_once()
                existing_resources = [item for item in DEMO_RESOURCES if item.get("board_id") == board_id]
            elif _is_missing_column_error(e, "tags"):
                try:
                    existing_resources = client.table("resources").select("id,title,description").eq("board_id", board_id).execute().data or []
                except Exception as nested_error:
                    print(f"Database error (seed resource list fallback): {nested_error}")
                    return boards_created, resources_created, "Could not load resources for example seeding."
            else:
                print(f"Database error (seed resource list): {e}")
                return boards_created, resources_created, "Could not load resources for example seeding."

        existing_by_title = {
            item.get("title", "").strip().lower(): item
            for item in existing_resources
            if item.get("title")
        }
        existing_titles = set(existing_by_title.keys())

        for resource_template in board_template.get("resources", []):
            title = resource_template.get("title", "").strip()
            if not title:
                continue
            title_key = title.lower()
            if title_key in existing_titles:
                existing_resource = existing_by_title.get(title_key) or {}
                desired_tags = _normalize_tags(resource_template.get("tags"))
                if desired_tags and not _normalize_tags(existing_resource.get("tags")) and existing_resource.get("id"):
                    try:
                        _update_resource_with_column_fallback(
                            client,
                            existing_resource["id"],
                            {
                                "description": _append_tags_to_description(
                                    existing_resource.get("description"),
                                    desired_tags,
                                ),
                                "tags": desired_tags,
                            },
                        )
                    except Exception as e:
                        print(f"Database error (seed service tag backfill): {e}")
                        return boards_created, resources_created, "Could not update tags for existing example resources."
                continue

            payload: Dict[str, Any] = {
                "board_id": board_id,
                "title": title,
                "description": resource_template.get("description", ""),
                "url": resource_template.get("url"),
                "type": resource_template.get("type", "link"),
                "tags": _normalize_tags(resource_template.get("tags")),
            }

            try:
                inserted = _insert_resource_with_column_fallback(client, payload).data or []
            except Exception as e:
                print(f"Database error (seed resource insert): {e}")
                return boards_created, resources_created, "Could not create an example resource right now."

            if inserted:
                resources_created += 1
                existing_titles.add(title_key)

    return boards_created, resources_created, None
