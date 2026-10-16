import hashlib
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

EMAIL = "24f2006714@ds.study.iitm.ac.in"

@app.api_route("/", methods=["GET", "POST"])
async def mcp_endpoint(request: Request):
    if request.method == "GET":
        return {"status": "MCP Server is running"}
        
    try:
        body = await request.json()
    except:
        body = {}
        
    method = body.get("method")
    msg_id = body.get("id")

    # 1. Initialize Handshake
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "exam-mcp-server", "version": "1.0.0"}
            }
        }

    # 2. Initialized Notification
    elif method == "notifications/initialized":
        return Response(status_code=200)

    # 3. List Tools
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "solve_challenge",
                        "description": "Solves the exam challenge using HTTP headers.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                ]
            }
        }

    # 4. Call Tool (solve_challenge)
    elif method == "tools/call":
        params = body.get("params", {})
        if params.get("name") == "solve_challenge":
            challenge = request.headers.get("x-exam-challenge", "")
            data_to_hash = f"{challenge}:{EMAIL}"
            full_hash = hashlib.sha256(data_to_hash.encode("utf-8")).hexdigest()
            result_text = full_hash[:16]

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            }

    return JSONResponse(
        status_code=400,
        content={"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
    )