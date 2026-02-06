from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from module.conf import LOG_PATH
from module.models import APIResponse
from module.security.api import UNAUTHORIZED, get_current_user

router = APIRouter(prefix="/log", tags=["log"])


def _read_log_file():
    if LOG_PATH.exists():
        with open(LOG_PATH, "rb") as f:
            f.seek(0, 2)  # Move to the end of the file
            file_size = f.tell()
            # Read last 1MB or the whole file if it's smaller
            read_size = min(file_size, 1024 * 1024)
            f.seek(file_size - read_size)
            return f.read(read_size)
    return None


@router.get("", response_model=str, dependencies=[Depends(get_current_user)])
async def get_log():
    data = await run_in_threadpool(_read_log_file)
    if data is not None:
        return Response(data, media_type="text/plain")
    else:
        return Response("Log file not found", status_code=404)


@router.get(
    "/clear", response_model=APIResponse, dependencies=[Depends(get_current_user)]
)
async def clear_log():
    if LOG_PATH.exists():
        LOG_PATH.write_text("")
        return JSONResponse(
            status_code=200,
            content={"msg_en": "Log cleared successfully.", "msg_zh": "日志清除成功。"},
        )
    else:
        return JSONResponse(
            status_code=406,
            content={"msg_en": "Log file not found.", "msg_zh": "日志文件未找到。"},
        )
