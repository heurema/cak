# P0 Pain Sources

Date: 2026-06-10

This is an initial source ledger for the P0 pains in
[`docs/01_pain_map.md`](../docs/01_pain_map.md). It is not complete proof of
market demand. It separates verified public sources from assumptions that still
need interviews, incident writeups, or production traces.

## Source ledger

| ID | Source | Status | Why it matters |
|---|---|---|---|
| SRC-NIST-AI-RMF | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | HTTP 200 checked 2026-06-10 | Supports need for mapped, measured, managed AI risk |
| SRC-OTEL-GENAI | [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | HTTP 200 checked 2026-06-10 | Shows industry need for GenAI trace semantics |
| SRC-OWASP-PI | [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | HTTP 200 checked 2026-06-10 | Supports external instruction and tool-use attack risk |
| SRC-REFLEXION | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | HTTP 200 checked 2026-06-10 | Shows research demand for agents learning from prior attempts |
| SRC-VOYAGER | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | HTTP 200 checked 2026-06-10 | Shows skill-library style agent learning as a research pattern |
| SRC-OPENAI-TOOLS | [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling) | HTTP 200 checked 2026-06-10 | Demonstrates provider-specific tool call semantics |
| SRC-ANTHROPIC-TOOLS | [Anthropic tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) | HTTP 200 checked 2026-06-10 | Demonstrates provider-specific tool call semantics |
| SRC-GEMINI-TOOLS | [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) | HTTP 200 checked 2026-06-10 | Demonstrates provider-specific tool call semantics |
| SRC-ANTHROPIC-PRICING | [Anthropic pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) | HTTP 200 checked 2026-06-10 | Supports cost modeling and provider-cost variance |
| SRC-MCP-INTRO | [Model Context Protocol introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | HTTP 200 checked 2026-06-10 | Supports MCP gateway/proxy as a low-friction tool-boundary form factor |

## P0 mapping

### P0.1 Agent behavior is not governable

Relevant sources:

- SRC-NIST-AI-RMF
- SRC-OTEL-GENAI

Evidence status: partially supported. Public standards activity supports the
need for AI risk and trace semantics, but CAK still needs user interviews and
real incidents showing where existing traces fail.

### P0.2 Agents repeat mistakes instead of learning safely

Relevant sources:

- SRC-REFLEXION
- SRC-VOYAGER

Evidence status: research-supported, not market-validated. These sources show
that learning from prior attempts is an active research pattern. CAK still needs
production examples where unsafe or stale learning caused harm.

### P0.3 Unsafe external actions

Relevant sources:

- SRC-OWASP-PI
- SRC-OPENAI-TOOLS
- SRC-ANTHROPIC-TOOLS
- SRC-GEMINI-TOOLS

Evidence status: partially supported. Tool-use APIs and prompt-injection risks
show the attack surface. CAK still needs concrete incidents or user traces where
external tool actions created unacceptable risk.

### P0.4 Cost is unpredictable

Relevant sources:

- SRC-ANTHROPIC-PRICING

Evidence status: weakly supported. Provider pricing supports the need for cost
models, but CAK needs observed agent traces showing how retries, tool calls,
long context, and shadow evals affect real cost.

### P0.5 Vendor lock-in

Relevant sources:

- SRC-OPENAI-TOOLS
- SRC-ANTHROPIC-TOOLS
- SRC-GEMINI-TOOLS

Evidence status: supported at API-shape level. The next proof needed is a
portability test showing the same task capsule across providers and where
semantics diverge.

## Evidence gaps

- User interviews for the first target segment.
- Public postmortems or internal incident notes for unsafe agent actions.
- Real trace samples with approval, denial, retry, and cost outcomes.
- Baseline comparison against existing tracing and policy tools.
- Evidence that developers value CAK for debugging, not only compliance.

