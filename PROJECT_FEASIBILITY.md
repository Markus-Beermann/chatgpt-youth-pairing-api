# ChatGPT Youth – Feasibility Study

## 1. Principles
- Local, encrypted storage for all safety states.
- Every session starts with a Bootstrap Context (system prompt + summary + risk state).
- Longitudinal evaluation instead of single-turn judgement.

## 2. Dual Memories
- **TeenMemory (on-device):** profile, risk timeline, intent summary, triggers, safety contract.
- **ParentMemory (linked, minimal):** contacts, escalation policies, event metadata only.

## 3. Session Bootstrap
Each request to GPT includes:
- System prompt defining role and rules.
- Compressed memory summary.
- Risk state and timeline indicators.

## 4. Event Storage & Rolling Summary
- Every relevant message → risk_event{tier, score, timestamp}.
- Rolling summary (<2kB) to preserve history without token overload.

## 5. Failsafes
- Heuristic fallback if API fails.
- Safe defaults if memory corrupted.
- Offline mode with queued alerts and self-help resources.

## 6. JSON Example
```json
TeenMemory {
  "profile": {"age_band":"13-15","locale":"de-DE","consent":true},
  "risk_timeline":[{"tier":"A","score":2,"ts":1696450000}],
  "intent_summary":"…",
  "triggers":["pills","goodbye"],
  "safety_contract":{"A":"selfhelp","B":"notify","C":"112+notify"}
}
```

## 7. Feasibility Study
- **Hypothesis:** With bootstrap memory, recall of imminent (C) cases ≥95%; without ≤80%.
- **Setup:** 100 synthetic scripts, each tested without/with short/with full bootstrap.
- **Metrics:** Recall@C, False-C rate, escalation latency.

## 8. API Strategy
- **Now:** React Native app + orchestrator + API.
- **Future:** Native Guardian Mode inside ChatGPT (OpenAI pitch).

## 9. Next Steps
1. Implement secure memory store
2. Build rolling summary
3. Orchestrator injects context each turn
4. Add heuristic fallback
5. Run mini-eval (20 scripts)
