---
title: LLM Landscape Cheat Sheet — April 12, 2026
type: reference
depth_score: 4
depth_signals:
  file_size_kb: 5.7
  content_chars: 5414
  entity_count: 0
  slide_count: 0
  sheet_count: 0
  topic_count: 0
  has_summary: 0
vocab_density: 0.74
source: Graeme @gkisokay, Hermes + OpenClaw community
captured: 2026-04-12
relevance: high — informs model selection for Knowledge Engine retrieval, synthesis, and always-on processing
---
# LLM Landscape — April 12, 2026

Source: Graeme @gkisokay, Hermes + OpenClaw Agents community

## Tier 1 — Frontier
| Model | Key Claim | Price | License | Relevance to Brien |
|-------|-----------|-------|---------|-------------------|
| Claude Opus 4.6 | #1 agentic terminal coding | Premium | Proprietary | Current primary — synthesis, Opus passes |
| GPT-5.4 | Superhuman computer use, real planning | $100/mo plan | Proprietary | Potential for desktop automation |
| GLM-5.1 | #1 SWE-Pro, 8hr autonomous execution | Cheaper than Opus input | MIT | **HIGH: MIT license + 8hr autonomy = self-hosted retrieval** |

## Tier 2 — Execution
| Model | Key Claim | Notes |
|-------|-----------|-------|
| MiniMax M2.7 | 97% skill adherence | API only |
| Kimi K2.5 | Long-horizon stability, agent swarm | Worth watching for retrieval |
| Grok 4.20 | Lowest hallucination, 16 parallel agents, 2M context | **HIGH: native multi-agent for parallel sweeps** |
| DeepSeek V3.2 | Frontier reasoning at 1/50th cost | Cost-efficient for high-volume retrieval |

## Tier 3 — Balanced
| Model | Key Claim | Notes |
|-------|-----------|-------|
| Claude Sonnet 4.6 | 98% of Opus at 1/5 cost | Current workhorse for retrieval tasks |
| GPT-5.4 mini | 93.4% tool-call reliability | Potential retrieval alternative |
| Gemini 3.1 Pro | Best multimodal value | Useful for video/audio persona sources |
| Qwen3.6 Plus | Near-frontier coding, free via OpenRouter | **HIGH: free retrieval at near-frontier quality** |
| Llama 4 Maverick | Open-weight, zero marginal cost | **HIGH: self-host for unlimited retrieval** |
| Mistral Small 4 | One model replacing three, Apache 2.0 | Efficient for mixed workloads |

## Tier 4 — Local ($0, runs on 32GB RAM)
| Model | Key Claim | RAM | Notes |
|-------|-----------|-----|-------|
| Qwen3.5-9B | Always-on subconscious loop | 16GB | **HIGH: always-on Notice phase processor** |
| Qwen3.5-27B | Stronger instruction following | 32GB | Better quality local model |
| Gemma 4 31B | Best local reasoning, Apache 2.0 | 32GB | Commercial-ready |
| DeepSeek R1 distill | Best chain-of-thought at $0 | varies | Reasoning tasks |
| GLM-4.5-Air | Purpose-built for agent tool use | varies | **HIGH: designed for tool calling** |

## Strategic Implications for Intent/Knowledge Engine

### Model Mixing Architecture
Intent already prescribes model mixing (Haiku for capture, Sonnet for spec, Opus for review). The landscape suggests a refined stack:

| Task | Current | Potential Optimization |
|------|---------|----------------------|
| Retrieval (web crawling, content fetch) | Sonnet via Cowork dispatch | Llama 4 Maverick (self-hosted, $0) or Qwen3.6 Plus (free via OpenRouter) |
| Content conversion to markdown | Sonnet | GLM-5.1 (MIT, 8hr autonomy) or DeepSeek V3.2 (1/50th cost) |
| Synthesis (voice analysis, reasoning chains) | Opus | Keep Opus — synthesis quality is non-negotiable |
| Always-on signal processing | Not implemented | Qwen3.5-9B local (16GB, always-on) |
| Parallel sweep orchestration | Cowork dispatch (serial) | Grok 4.20 (native 16 parallel agents) |

### Volume Unlock
If retrieval moves to self-hosted or free-tier models, the constraint shifts from API cost to network bandwidth and storage. The cortege retrieval pattern could run continuously instead of in prompted batches.

---

## NVIDIA NIM API — Free Serverless Inference Gateway

**URL:** https://build.nvidia.com
**API Endpoint:** https://integrate.api.nvidia.com/v1
**Cost:** Free (rate-limited)
**Compatibility:** OpenAI-compatible API — works with LiteLLM, OpenRouter, any OpenAI client

### What It Provides
80+ models accessible through a single OpenAI-compatible endpoint, including DeepSeek, Kimi, GLM, MiniMax, and Zhipu AI. No GPU management, no API credits during prototyping. Phone verification required for API key.

### Relevance to Brien's Pipeline

**Best for:** Multi-armed bandit testing of pipeline configurations. The persona product spec (SPEC-persona-product-system.md) defines six bandit arms — different model-pipeline combinations for persona compilation. NVIDIA NIM provides free access to multiple models through one endpoint, enabling zero-cost A/B testing of pipeline configurations against the shared (non-confidential) persona library.

**Not suitable for:**
- Production retrieval sweeps (rate limits too restrictive for 170-persona overnight runs)
- Engagement-specific content (NVIDIA logs prompts for model improvement — confidentiality concern)
- High-throughput work (slower during peak hours)

### Integration Path
LiteLLM proxy adds NVIDIA NIM as one more backend alongside OpenRouter, direct provider APIs, and local Ollama. Zero additional integration work — just add the base_url and API key to the proxy config.

### Setup
1. Get API key at https://build.nvidia.com (phone verification)
2. Set base_url to https://integrate.api.nvidia.com/v1
3. Use standard OpenAI client — models appear as nvidia/* in the proxy

### Position in Model Mixing Architecture
| Use Case | Provider | Why |
|----------|----------|-----|
| Synthesis (Opus-quality) | Anthropic direct | Non-negotiable quality |
| Production retrieval | OpenRouter / direct providers | Rate limits, throughput |
| Local autonomous | GLM-5.1 via Ollama | Zero cost, no logging |
| Pipeline testing / bandit arms | NVIDIA NIM | Free, 80+ models, zero commitment |
