"""Small MCP stdio transport helpers.

The v0.1 examples use newline-delimited JSON-RPC because it is easy to read in
tests. Real MCP stdio clients use `Content-Length` framed JSON messages. These
helpers support both formats so the gateway can remain compatible with the
readable demo harness and with existing agent stacks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import IO, Any


@dataclass(slots=True)
class StdioMessage:
    payload: bytes
    framed: bool


def _content_length(header_line: bytes) -> int:
    try:
        _, value = header_line.split(b":", 1)
        return int(value.strip())
    except ValueError as exc:
        raise ValueError(f"invalid MCP Content-Length header: {header_line!r}") from exc


def read_message(stream: IO[bytes]) -> StdioMessage | None:
    """Read one JSON payload from newline JSON-RPC or MCP stdio framing."""
    while True:
        first = stream.readline()
        if first == b"":
            return None
        if first.strip():
            break

    if first.lower().startswith(b"content-length:"):
        length = _content_length(first)
        while True:
            header = stream.readline()
            if header in (b"\r\n", b"\n", b""):
                break
            if header.lower().startswith(b"content-length:"):
                length = _content_length(header)
        return StdioMessage(stream.read(length), framed=True)

    return StdioMessage(first, framed=False)


def encode_message(message: dict[str, Any], framed: bool) -> bytes:
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    if framed:
        return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body
    return body + b"\n"


def write_message(stream: IO[bytes], message: dict[str, Any], framed: bool) -> None:
    stream.write(encode_message(message, framed))
    stream.flush()
