import os
from urllib.parse import urlencode
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, Request, Form, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Import database functions from db.py
import db

app = FastAPI(title="Team Resource Board")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Supabase auth config
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
SUPABASE_STORAGE_BUCKET: str = os.getenv("SUPABASE_STORAGE_BUCKET", "resource-files")
RESOURCE_TYPES = ("all", "link", "file", "image", "video")


def get_storage_client():
    key = SUPABASE_SERVICE_KEY or SUPABASE_KEY
    if not SUPABASE_URL or not key:
        return None
    try:
        return create_client(SUPABASE_URL, key)
    except Exception:
        return None


def _signed_url_to_absolute(url: str) -> str:
    if not url:
        return url
    if url.startswith("http"):
        return url
    if url.startswith("/"):
        return f"{SUPABASE_URL}/storage/v1{url}"
    return f"{SUPABASE_URL}/storage/v1/{url}"


async def _upload_to_storage(uploaded_file: UploadFile) -> tuple[str | None, str | None]:
    if not uploaded_file or not uploaded_file.filename:
        return None, None

    storage_client = get_storage_client()
    if not storage_client:
        return None, "Storage client is not configured."

    try:
        file_bytes = await uploaded_file.read()
        if not file_bytes:
            return None, "Uploaded file is empty."

        extension = Path(uploaded_file.filename).suffix
        file_path = f"resources/{uuid4()}{extension}"
        content_type = uploaded_file.content_type or "application/octet-stream"
        storage_client.storage.from_(SUPABASE_STORAGE_BUCKET).upload(
            path=file_path,
            file=file_bytes,
            file_options={"content-type": content_type},
        )
        return file_path, None
    except Exception as e:
        print(f"Storage upload error: {e}")
        return None, "Could not upload file to storage."


def _delete_from_storage(storage_path: str | None) -> None:
    if not storage_path:
        return
    storage_client = get_storage_client()
    if not storage_client:
        return
    try:
        storage_client.storage.from_(SUPABASE_STORAGE_BUCKET).remove([storage_path])
    except Exception as e:
        print(f"Storage delete warning: {e}")


def _normalize_resource_type(resource_type: str | None) -> str:
    normalized = (resource_type or "all").strip().lower()
    if normalized not in RESOURCE_TYPES:
        return "all"
    return normalized


def _build_board_url(
    board_id: str,
    message: str | None = None,
    error: str | None = None,
    resource_type: str = "all",
    tag: str = "",
) -> str:
    params: dict[str, str] = {}
    normalized_type = _normalize_resource_type(resource_type)
    cleaned_tag = (tag or "").strip()

    if message:
        params["message"] = message
    if error:
        params["error"] = error
    if normalized_type != "all":
        params["type"] = normalized_type
    if cleaned_tag:
        params["tag"] = cleaned_tag

    query = urlencode(params)
    if query:
        return f"/board/{board_id}?{query}"
    return f"/board/{board_id}"


def _extract_tags_from_description(description: str | None) -> tuple[str, list[str]]:
    raw_description = (description or "").strip()
    if "Tags:" not in raw_description:
        return raw_description, []
    base, _, tag_text = raw_description.partition("Tags:")
    cleaned_base = base.rstrip(" |").strip()
    tags = [item.strip() for item in tag_text.split(",") if item.strip()]
    return cleaned_base, tags

async def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    try:
        # We can use a temporary client to verify the user
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = client.auth.get_user(access_token)
        return res.user
    except Exception:
        return None

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = await get_current_user(request)
    access_token = request.cookies.get("access_token")
    message = request.query_params.get("message")
    error = request.query_params.get("error")
    
    # Fetch boards using db layer
    boards = db.get_all_boards(access_token)
        
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request, 
        "boards": boards,
        "user": user,
        "message": message,
        "error": error,
    })


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/boards/create")
async def create_board(request: Request, name: str = Form(...), description: str = Form("")):
    access_token = request.cookies.get("access_token")
    board, error = db.create_board(name=name, description=description, access_token=access_token)

    if error:
        query = urlencode({"error": error})
        return RedirectResponse(url=f"/?{query}", status_code=status.HTTP_303_SEE_OTHER)

    if board and board.get("id"):
        return RedirectResponse(url=f"/board/{board['id']}", status_code=status.HTTP_303_SEE_OTHER)

    query = urlencode({"message": "Board created."})
    return RedirectResponse(url=f"/?{query}", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/boards/seed-examples")
async def seed_examples(request: Request):
    access_token = request.cookies.get("access_token")
    boards_created, resources_created, error = db.seed_example_boards(access_token)

    if error:
        query = urlencode({"error": error})
        return RedirectResponse(url=f"/?{query}", status_code=status.HTTP_303_SEE_OTHER)

    message = f"Example data ready. Boards added: {boards_created}, resources added: {resources_created}."
    query = urlencode({"message": message})
    return RedirectResponse(url=f"/?{query}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="access_token", 
            value=res.session.access_token, 
            httponly=True,
            max_age=3600,
            samesite="lax"
        )
        return response
    except Exception as e:
        print(f"Login error: {e}")
        return templates.TemplateResponse(request=request, name="login.html", context={
            "request": request, 
            "error": "Invalid email or password"
        })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.get("/board/{board_id}", response_class=HTMLResponse)
async def board_view(request: Request, board_id: str):
    user = await get_current_user(request)
    access_token = request.cookies.get("access_token")
    message = request.query_params.get("message")
    error = request.query_params.get("error")
    selected_type = _normalize_resource_type(request.query_params.get("type"))
    selected_tag = (request.query_params.get("tag") or "").strip()
    
    # Fetch board details
    board = db.get_board_by_id(board_id, access_token)
    
    if not board:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
    # Fetch resources for this board
    all_resources = db.get_resources_by_board(board_id, access_token)
    available_tags_set: set[str] = set()
    for resource in all_resources:
        if resource.get("storage_path"):
            resource["view_url"] = f"/resources/{resource['id']}/open"
            resource["has_file"] = True
        else:
            resource["view_url"] = resource.get("url")
            resource["has_file"] = False

        clean_description, inferred_tags = _extract_tags_from_description(resource.get("description"))
        resource["description"] = clean_description

        raw_tags = resource.get("tags") or ""
        if not raw_tags and inferred_tags:
            raw_tags = ", ".join(inferred_tags)
        tag_list = [item.strip() for item in raw_tags.split(",") if item.strip()]
        resource["tag_list"] = tag_list
        for tag in tag_list:
            available_tags_set.add(tag)

    resources = all_resources
    if selected_type != "all":
        resources = [item for item in resources if item.get("type") == selected_type]
    if selected_tag:
        selected_tag_lower = selected_tag.lower()
        resources = [
            item
            for item in resources
            if any(tag.lower() == selected_tag_lower for tag in item.get("tag_list", []))
        ]

    filter_links = {
        resource_type: _build_board_url(board_id=board_id, resource_type=resource_type, tag=selected_tag)
        for resource_type in RESOURCE_TYPES
    }
    available_tags = sorted(available_tags_set, key=lambda item: item.lower())
    tag_links = {
        tag: _build_board_url(board_id=board_id, resource_type=selected_type, tag=tag)
        for tag in available_tags
    }
    clear_tag_link = _build_board_url(board_id=board_id, resource_type=selected_type)
    share_url = str(request.url_for("board_view", board_id=board_id))

    return templates.TemplateResponse(request=request, name="board.html", context={
        "request": request, 
        "board": board, 
        "resources": resources,
        "selected_type": selected_type,
        "selected_tag": selected_tag,
        "filter_links": filter_links,
        "available_tags": available_tags,
        "tag_links": tag_links,
        "clear_tag_link": clear_tag_link,
        "share_url": share_url,
        "user": user,
        "message": message,
        "error": error,
    })


@app.post("/board/{board_id}/share")
async def update_board_share_settings(
    request: Request,
    board_id: str,
    make_public: str = Form("false"),
    active_type: str = Form("all"),
    active_tag: str = Form(""),
):
    access_token = request.cookies.get("access_token")
    normalized_active_type = _normalize_resource_type(active_type)
    normalized_active_tag = (active_tag or "").strip()
    is_public = str(make_public).strip().lower() == "true"

    _, error = db.set_board_visibility(board_id=board_id, is_public=is_public, access_token=access_token)
    if error:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error=error,
                resource_type=normalized_active_type,
                tag=normalized_active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    message = "Share link enabled. Anyone with this link can open the board." if is_public else "Share link disabled for public users."
    return RedirectResponse(
        url=_build_board_url(
            board_id,
            message=message,
            resource_type=normalized_active_type,
            tag=normalized_active_tag,
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.get("/resources/{resource_id}/open")
async def open_resource_file(request: Request, resource_id: str):
    access_token = request.cookies.get("access_token")
    resource = db.get_resource_by_id(resource_id, access_token)
    if not resource:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    board_id = resource.get("board_id", "")
    storage_path = resource.get("storage_path")
    if not storage_path:
        if resource.get("url"):
            return RedirectResponse(url=resource["url"], status_code=status.HTTP_303_SEE_OTHER)
        query = urlencode({"error": "No file is attached to this resource."})
        return RedirectResponse(url=f"/board/{board_id}?{query}", status_code=status.HTTP_303_SEE_OTHER)

    storage_client = get_storage_client()
    if not storage_client:
        query = urlencode({"error": "Storage client is not configured."})
        return RedirectResponse(url=f"/board/{board_id}?{query}", status_code=status.HTTP_303_SEE_OTHER)

    try:
        signed = storage_client.storage.from_(SUPABASE_STORAGE_BUCKET).create_signed_url(storage_path, 600)
        signed_url = getattr(signed, "signedURL", None) or getattr(signed, "signedUrl", None)
        if not signed_url and isinstance(signed, dict):
            signed_url = signed.get("signedURL") or signed.get("signedUrl")
        if not signed_url:
            raise ValueError("Missing signed URL in storage response")
        return RedirectResponse(url=_signed_url_to_absolute(signed_url), status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Storage signed URL error: {e}")
        query = urlencode({"error": "Could not open file right now."})
        return RedirectResponse(url=f"/board/{board_id}?{query}", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/board/{board_id}/resources/create")
async def create_resource(
    request: Request,
    board_id: str,
    title: str = Form(...),
    description: str = Form(""),
    resource_type: str = Form("link"),
    url: str = Form(""),
    tags: str = Form(""),
    active_type: str = Form("all"),
    active_tag: str = Form(""),
    uploaded_file: UploadFile | None = File(None),
):
    access_token = request.cookies.get("access_token")
    normalized_active_type = _normalize_resource_type(active_type)
    normalized_url = url.strip() or None
    storage_path, upload_error = await _upload_to_storage(uploaded_file)
    if upload_error:
        return RedirectResponse(
            url=_build_board_url(board_id, error=upload_error, resource_type=normalized_active_type, tag=active_tag),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    effective_type = resource_type
    if storage_path and resource_type == "link":
        effective_type = "file"

    if effective_type == "link" and not normalized_url:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error="URL is required for link resources.",
                resource_type=normalized_active_type,
                tag=active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    if not normalized_url and not storage_path:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error="Provide a URL or upload a file.",
                resource_type=normalized_active_type,
                tag=active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    _, error = db.create_resource(
        board_id=board_id,
        title=title,
        description=description,
        url=normalized_url,
        resource_type=effective_type,
        storage_path=storage_path,
        tags=tags,
        access_token=access_token,
    )

    if error:
        _delete_from_storage(storage_path)
        return RedirectResponse(
            url=_build_board_url(board_id, error=error, resource_type=normalized_active_type, tag=active_tag),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url=_build_board_url(board_id, message="Resource created.", resource_type=normalized_active_type, tag=active_tag),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.post("/board/{board_id}/resources/{resource_id}/update")
async def update_resource(
    request: Request,
    board_id: str,
    resource_id: str,
    title: str = Form(...),
    description: str = Form(""),
    resource_type: str = Form("link"),
    url: str = Form(""),
    tags: str = Form(""),
    active_type: str = Form("all"),
    active_tag: str = Form(""),
    uploaded_file: UploadFile | None = File(None),
):
    access_token = request.cookies.get("access_token")
    normalized_active_type = _normalize_resource_type(active_type)
    current = db.get_resource_by_id(resource_id, access_token)
    if not current:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error="Resource not found.",
                resource_type=normalized_active_type,
                tag=active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    normalized_url = url.strip() or None
    new_storage_path, upload_error = await _upload_to_storage(uploaded_file)
    if upload_error:
        return RedirectResponse(
            url=_build_board_url(board_id, error=upload_error, resource_type=normalized_active_type, tag=active_tag),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    effective_storage_path = current.get("storage_path")
    if new_storage_path:
        effective_storage_path = new_storage_path

    effective_type = resource_type
    if effective_storage_path and resource_type == "link":
        effective_type = "file"

    if effective_type == "link" and not normalized_url:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error="URL is required for link resources.",
                resource_type=normalized_active_type,
                tag=active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    if not normalized_url and not effective_storage_path:
        return RedirectResponse(
            url=_build_board_url(
                board_id,
                error="Provide a URL or upload a file.",
                resource_type=normalized_active_type,
                tag=active_tag,
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    _, error = db.update_resource(
        resource_id=resource_id,
        title=title,
        description=description,
        url=normalized_url,
        resource_type=effective_type,
        storage_path=effective_storage_path,
        tags=tags,
        access_token=access_token,
    )
    if error:
        if new_storage_path:
            _delete_from_storage(new_storage_path)
        return RedirectResponse(
            url=_build_board_url(board_id, error=error, resource_type=normalized_active_type, tag=active_tag),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    if new_storage_path and current.get("storage_path") and current.get("storage_path") != new_storage_path:
        _delete_from_storage(current.get("storage_path"))

    return RedirectResponse(
        url=_build_board_url(board_id, message="Resource updated.", resource_type=normalized_active_type, tag=active_tag),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.post("/board/{board_id}/resources/{resource_id}/delete")
async def delete_resource(request: Request, board_id: str, resource_id: str):
    access_token = request.cookies.get("access_token")
    form = await request.form()
    active_type = _normalize_resource_type(form.get("active_type"))
    active_tag = (form.get("active_tag") or "").strip()
    current = db.get_resource_by_id(resource_id, access_token)
    deleted, error = db.delete_resource(resource_id=resource_id, access_token=access_token)
    if error:
        return RedirectResponse(
            url=_build_board_url(board_id, error=error, resource_type=active_type, tag=active_tag),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    storage_path = None
    if deleted:
        storage_path = deleted.get("storage_path")
    elif current:
        storage_path = current.get("storage_path")
    _delete_from_storage(storage_path)

    return RedirectResponse(
        url=_build_board_url(board_id, message="Resource deleted.", resource_type=active_type, tag=active_tag),
        status_code=status.HTTP_303_SEE_OTHER,
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
