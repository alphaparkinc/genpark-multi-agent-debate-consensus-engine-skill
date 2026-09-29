from client import MultiAgentDebateEngine

debate = MultiAgentDebateEngine(agents=["SecurityAgent", "PerformanceAgent", "ProductAgent"], rounds=2)
res = debate.run_debate(
    "Automated Zero-Downtime Database Migration",
    {"SecurityAgent": "Require manual approvals", "PerformanceAgent": "Direct batch migration", "ProductAgent": "Blue-green deploy"}
)

print("Synthesized Consensus:", res["consensus"])
print("Debate Rounds Completed:", len(res["rounds"]))
