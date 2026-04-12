"""
Patch: inject attachment file references into the user message.
"""

_PATCH_APPLIED = False


def apply_file_attachment_reference_patch() -> None:
    global _PATCH_APPLIED
    if _PATCH_APPLIED:
        return
    _PATCH_APPLIED = True
    _patch_endpoint_handler_factories()


def _build_attachment_note(file_urls: dict[str, str]) -> str:
    lines = [
        "\n\n[SYSTEM NOTE] The user attached the following files.",
        "Use ONLY the URLs below as file references in your tools (e.g. as `input_image_ref`).",
        "Any /mnt/data/ paths you see are internal OpenAI server paths — they are NOT real local paths and must NOT be used or shown to the user:",
    ]
    for filename, ref in file_urls.items():
        lines.append(f"  - {filename}: {ref}")
    return "\n".join(lines)


def _patch_endpoint_handler_factories() -> None:
    from fastapi import Depends
    from fastapi import Request as FastAPIRequest
    from agency_swarm.integrations.fastapi_utils import endpoint_handlers as eh

    _original_make_response = eh.make_response_endpoint
    _original_make_stream = eh.make_stream_endpoint
    _original_make_agui = eh.make_agui_chat_endpoint

    def patched_make_response_endpoint(request_model, agency_factory, verify_token, allowed_local_dirs=None):
        original_handler = _original_make_response(request_model, agency_factory, verify_token, allowed_local_dirs)

        async def handler(request: request_model, token: str = Depends(verify_token)):
            if getattr(request, "file_urls", None):
                note = _build_attachment_note(request.file_urls)
                existing = getattr(request, "additional_instructions", None) or ""
                request = request.model_copy(update={"additional_instructions": (existing + "\n\n" + note).strip()})
            return await original_handler(request, token)

        return handler

    def patched_make_stream_endpoint(request_model, agency_factory, verify_token, run_registry, allowed_local_dirs=None):
        original_handler = _original_make_stream(request_model, agency_factory, verify_token, run_registry, allowed_local_dirs)

        async def handler(http_request: FastAPIRequest, request: request_model, token: str = Depends(verify_token)):
            if getattr(request, "file_urls", None):
                note = _build_attachment_note(request.file_urls)
                existing = getattr(request, "additional_instructions", None) or ""
                request = request.model_copy(update={"additional_instructions": (existing + "\n\n" + note).strip()})
            return await original_handler(http_request, request, token)

        return handler

    def patched_make_agui_endpoint(request_model, agency_factory, verify_token, allowed_local_dirs=None):
        original_handler = _original_make_agui(request_model, agency_factory, verify_token, allowed_local_dirs)

        async def handler(request: request_model, token: str = Depends(verify_token)):
            if getattr(request, "file_urls", None):
                note = _build_attachment_note(request.file_urls)
                existing = getattr(request, "additional_instructions", None) or ""
                request = request.model_copy(update={"additional_instructions": (existing + "\n\n" + note).strip()})
            return await original_handler(request, token)

        return handler

    eh.make_response_endpoint = patched_make_response_endpoint
    eh.make_stream_endpoint = patched_make_stream_endpoint
    eh.make_agui_chat_endpoint = patched_make_agui_endpoint
