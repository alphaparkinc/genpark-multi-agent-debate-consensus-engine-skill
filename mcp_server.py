import sys
import json
from client import MultiAgentDebateEngine

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-multi-agent-debate-consensus-engine-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "orchestrate_agent_debate",
                        "description": "Simulate multi-round debate across multiple agent personas to reach consensus",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string", "description": "Subject of the debate"},
                                "agent_positions": {"type": "object", "description": "Mapping of agent names to initial positions"},
                                "rounds": {"type": "integer", "default": 2}
                            },
                            "required": ["topic", "agent_positions"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "orchestrate_agent_debate":
            top = args.get("topic", "")
            pos = args.get("agent_positions", {})
            r = args.get("rounds", 2)
            engine = MultiAgentDebateEngine(agents=list(pos.keys()), rounds=r)
            res = engine.run_debate(top, pos)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res)}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
