<div align="center">

<a href="https://github.com/intikhab49"><img src="assets/hero.svg" width="100%" alt="Intikhab Azam, AI/ML engineer, researcher and systems architect, painted in Pakistani truck art: reflective tape, two peacocks, a vase of roses, his name in Urdu and English, and swinging bumper chains."/></a>

</div>

<h1 align="center">Intikhab Azam · AI/ML Engineer, Researcher & Systems Architect</h1>

<p align="center"><b>Voice AI agents · RAG and LLM evaluation · multi-tenant SaaS · agentic coding · open-source developer tools</b></p>

I build AI systems that have to work in production: **voice agents** that answer real phone calls, **RAG and LLM agents** judged by cost per correct answer, and **multi-tenant SaaS platforms** with row-level security and field-level encryption. I also publish the research behind them, including the numbers that went against me, and open-source tools that catch problems before they ship: Microsoft gov-cloud gaps, broken Make.com scenarios, Postgres images that crash on older CPUs and packages an AI coding agent made up. Based in Pakistan, working with US teams, **open to contract work**. Website: [intikhab49.github.io](https://intikhab49.github.io/).

<img src="assets/road.svg" width="100%" alt="Animated Pakistani truck driving the Karakoram Highway past kilometre stones marked voice AI, RAG, LLM evals, ML, SaaS and open source."/>

## What I build

<img src="assets/services.svg" width="100%" alt="What I build: voice AI agents on Vapi and Twilio, RAG and LLM agents, LLM evals and research, multi-tenant SaaS architecture, agentic coding with Claude Code, Codex and DeepSeek, and automation with n8n and Cloudflare Workers."/>

- **AI voice agents**: Vapi and Twilio receptionists and outbound callers, wired into CRMs, payments and SMS
- **RAG and LLM agents**: knowledge-base chatbots with tool calling and memory, evaluated by cost per correct answer
- **LLM evals and research**: calibration, benchmarks and backtests that report the losing numbers too
- **Multi-tenant SaaS architecture**: Postgres row-level security, BFF auth, field-level encryption, event-driven jobs
- **Agentic coding**: Claude Code, Codex and DeepSeek working in parallel behind spec files, a claims board and test gates
- **Automation and data pipelines**: n8n, Cloudflare Workers, lead generation, scraping and enrichment
- **Developer tools and CI checks**: CLIs, GitHub Actions and MCP servers on PyPI and npm, for Microsoft gov clouds (GCC High, Azure Government), Make.com, Postgres images and AI-written code

## Open-source AI projects

### New in October 2026

| Tool | What it does | Get it |
| --- | --- | --- |
| [fairfax](https://github.com/intikhab49/fairfax) | **Is it available in GCC High?** Checks a Microsoft 365 GCC, GCC High or DoD and Azure Government plan against Microsoft's own feature availability tables (633 features, every row cited), and finds commercial endpoints in your code | `pip install fairfax` · [website](https://intikhab49.github.io/fairfax/) · [GitHub Action](https://github.com/marketplace/actions/fairfax-gov-cloud-check) |
| [blueprint-runtime](https://github.com/intikhab49/blueprint-runtime) | **Test Make.com scenarios offline.** Runs exported Make (Integromat) blueprints locally and replays real Make runs, so a broken mapping fails in CI instead of in production. 71 of 79 real runs reproduced exactly | `npm install -g blueprint-runtime` · [website](https://intikhab49.github.io/blueprint-runtime/) |
| [lifeboat](https://github.com/intikhab49/lifeboat) | **A Bitnami PostgreSQL alternative.** Bitnami's PostgreSQL and PostgreSQL HA (repmgr) images rebuilt from upstream source: same paths, scripts and env vars, drop-in for the Bitnami Helm charts | `ghcr.io/intikhab49/lifeboat` |
| [pgvector-cpu-check](https://github.com/intikhab49/pgvector-cpu-check) | **Which CPU crashes your Postgres image?** Runs it on 7 CPUs, from a 2008 Intel to Raspberry Pi and Graviton2, and names the faulting instruction (SIGILL) | [GitHub Action](https://github.com/marketplace/actions/pgvector-cpu-check) · [website](https://intikhab49.github.io/pgvector-cpu-check/) |
| [pdf-cpu-bench](https://github.com/intikhab49/pdf-cpu-bench) | **Best PDF parser for RAG without a GPU.** 9 PDF-to-Markdown parsers on a plain 4-core CPU: olmocr-bench accuracy, seconds per page, peak RAM, install size | Benchmark and results |
| [whofetched](https://github.com/intikhab49/whofetched) | **Which AI actually read your page?** Secret canary links plus a Cloudflare Worker log, tested on ChatGPT, Claude, Gemini, Grok, Perplexity and Copilot | Cloudflare Worker |

<p align="center">
  <a href="https://github.com/intikhab49/open-jev-typed-decision-engine"><img src="assets/cards/open-jev.svg" width="49%" alt="Open Jev: open-source typed decision engine. A 150M model reproduces TypeSafe Jev with calibrated confidence: 0.697 vs 0.727 accuracy, 2.5x better calibrated, 4x faster, free."/></a>
  <a href="https://github.com/intikhab49/pushback"><img src="assets/cards/pushback.svg" width="49%" alt="pushback: CLI that measures how often you correct your Claude Code agent, drafts CLAUDE.md rules and exports DPO preference pairs."/></a>
  <a href="https://github.com/intikhab49/diff-gate"><img src="assets/cards/diff-gate.svg" width="49%" alt="diff-gate: Claude Code skill and GitHub Action that fails on AI-hallucinated package imports, a defence against slopsquatting."/></a>
  <a href="https://github.com/intikhab49/rag-cost-curve"><img src="assets/cards/rag-cost-curve.svg" width="49%" alt="rag-cost-curve: benchmark of cost per correct answer for agentic, iterative, reranked and naive RAG on multi-hop QA. Agentic RAG: +32.5 exact match at 2.5x the cost."/></a>
  <a href="https://github.com/intikhab49/minio-from-source"><img src="assets/cards/minio-from-source.svg" width="49%" alt="minio-from-source: free MinIO Docker image built from source at pinned releases, multi-arch amd64 and arm64 on GHCR, smoke-tested."/></a>
  <a href="https://github.com/intikhab49/vapi-voice-agent-crm"><img src="assets/cards/voice-agent-crm.svg" width="49%" alt="Vapi voice agent CRM: call-ops backend for AI voice agents with webhooks, predictive dialer, auto-redial and Stripe-verified conversions."/></a>
  <a href="https://github.com/intikhab49/edgeproof-crypto-trading-backtest"><img src="assets/cards/edgeproof.svg" width="49%" alt="EdgeProof: crypto trading backtesting and ML validation with triple-barrier labels, purged k-fold CV and deflated Sharpe. Result: no edge after fees."/></a>
  <a href="https://github.com/intikhab49/local-business-lead-finder"><img src="assets/cards/lead-finder.svg" width="49%" alt="Local business lead finder: self-hosted lead generation past the Google Places 60-result cap, with an OpenStreetMap fallback and e-mail enrichment."/></a>
</p>

<details>
<summary><b>All current repositories, with details</b></summary>
<br/>

| Repository | What it is | Stack |
| --- | --- | --- |
| [fairfax](https://github.com/intikhab49/fairfax) | Is it available in GCC High? Checks a Microsoft 365 GCC / GCC High / DoD and Azure Government plan against Microsoft's own availability tables, scans code for wrong-cloud endpoints | Python · PyPI · GitHub Action · MCP |
| [blueprint-runtime](https://github.com/intikhab49/blueprint-runtime) | Offline test runner for Make.com (Integromat) scenario blueprints: replays real Make runs and catches broken mappings in CI | TypeScript · npm · CLI |
| [lifeboat](https://github.com/intikhab49/lifeboat) | Drop-in Bitnami PostgreSQL and PostgreSQL HA (repmgr) images rebuilt from upstream source, amd64 + arm64 | Docker · Helm · GHCR |
| [pgvector-cpu-check](https://github.com/intikhab49/pgvector-cpu-check) | Runs a Postgres image on 7 CPUs and names the instruction that crashes it (SIGILL) | Python · QEMU · GitHub Action |
| [pdf-cpu-bench](https://github.com/intikhab49/pdf-cpu-bench) | 9 PDF-to-Markdown parsers for RAG on a 4-core CPU: accuracy, seconds per page, RAM, install size | Python · Docling · MinerU · Marker |
| [whofetched](https://github.com/intikhab49/whofetched) | Proves which AI fetched your page with secret canary links and a Cloudflare Worker log | JavaScript · Cloudflare Workers |
| [open-jev-typed-decision-engine](https://github.com/intikhab49/open-jev-typed-decision-engine) | Open reproduction of TypeSafe Jev: a 150M typed decision engine (noul / choice / score) with calibrated confidence | Python · PyTorch · ModernBERT |
| [pushback](https://github.com/intikhab49/pushback) | Measures how often you correct your Claude Code agent, drafts CLAUDE.md rules, exports DPO pairs | Python · CLI · PyPI |
| [minio-from-source](https://github.com/intikhab49/minio-from-source) | MinIO server + mc built from source at pinned releases, multi-arch images on GHCR | Docker · GitHub Actions |
| [diff-gate](https://github.com/intikhab49/diff-gate) | Fails on imports an AI coding agent invented, before attackers can register them | JavaScript · GitHub Action |
| [rag-cost-curve](https://github.com/intikhab49/rag-cost-curve) | Cost per correct answer for agentic, iterative, reranked and naive RAG on MuSiQue | Python · Claude |
| [edgeproof-crypto-trading-backtest](https://github.com/intikhab49/edgeproof-crypto-trading-backtest) | Backtesting and ML validation: triple-barrier labels, purged CV, deflated Sharpe, a planted-edge control | Python · LightGBM · PyTorch |
| [local-business-lead-finder](https://github.com/intikhab49/local-business-lead-finder) | Lead generation past the Google Places cap, OpenStreetMap fallback, e-mail enrichment | Python · FastAPI · Streamlit |
| [vapi-voice-agent-crm](https://github.com/intikhab49/vapi-voice-agent-crm) | CRM and call-ops backend for Vapi voice agents: webhooks, predictive dialer, Stripe-verified conversions | Node.js · Express · Twilio · Stripe |
| [secureface-liveness-detection](https://github.com/intikhab49/secureface-liveness-detection) | Face recognition access control with head-pose liveness, rPPG pulse detection and ChromaDB matching | InsightFace · OpenCV · Streamlit |
| [ai-wealth-advisor](https://github.com/intikhab49/ai-wealth-advisor) | RAG + tool-calling financial assistant: VaR, Sharpe, drawdown, diversification scoring | LangChain · Gemini · Flask |
| [cryptoaion-price-prediction](https://github.com/intikhab49/cryptoaion-price-prediction) | BiLSTM + attention crypto price prediction API with WebSocket streaming and JWT auth | PyTorch · FastAPI |
| [npi-healthcare-lead-pipeline](https://github.com/intikhab49/npi-healthcare-lead-pipeline) | NPI Registry to practice websites to e-mails, resumable and scheduled on GitHub Actions | Python · GitHub Actions |
| [libncurses5-libaio1-ubuntu-deb](https://github.com/intikhab49/libncurses5-libaio1-ubuntu-deb) | Legacy `libaio1` / `libncurses5` / `libtinfo5` `.deb` packages for newer Ubuntu | Ubuntu · dpkg |
| [git-notes](https://github.com/intikhab49/git-notes) | Working notes on git internals and GitHub Actions | Markdown |

</details>

<details>
<summary><b>Early projects (2023-2025, archived)</b></summary>
<br/>

Learning projects from before the work above. Kept public, read-only.

| Repository | What it is | Stack |
| --- | --- | --- |
| [crypto-price-prediction-api](https://github.com/intikhab49/crypto-price-prediction-api) | v1 of CryptoAion with BiLSTM and XGBoost research notebooks | FastAPI · PyTorch |
| [kubernetes-flask-microservices](https://github.com/intikhab49/kubernetes-flask-microservices) | Flask microservices on Kubernetes with NGINX, PostgreSQL, a logging service and Prometheus | Flask · Kubernetes · Docker |
| [kubernetes-flask-crud](https://github.com/intikhab49/kubernetes-flask-crud) | Flask + PostgreSQL behind NGINX on Minikube with NetworkPolicies | Flask · Kubernetes · NGINX |
| [flask-postgres-crud-dashboard](https://github.com/intikhab49/flask-postgres-crud-dashboard) | User management CRUD app with a Chart.js analytics dashboard | Flask · PostgreSQL · Docker |
| [react-express-drizzle-crud](https://github.com/intikhab49/react-express-drizzle-crud) | Full-stack TypeScript CRUD with Passport session auth | React · Express · Drizzle · Neon |
| [devops-agency-website](https://github.com/intikhab49/devops-agency-website) | DevOps agency site with a pricing calculator and contact API | React · TypeScript · Tailwind |
| [ubuntu-dev-tools-installer](https://github.com/intikhab49/ubuntu-dev-tools-installer) | Interactive Bash installer for Python, VS Code, Docker, Jenkins, kubectl | Bash |
| [cpp-queue-data-structure](https://github.com/intikhab49/cpp-queue-data-structure) | Array-based FIFO queue in C++ | C++ |

</details>

## System architecture

<img src="assets/architecture.svg" width="100%" alt="System architecture of a production AI platform as a painted route: callers and clients, Cloudflare Workers edge with BFF auth, NestJS and FastAPI services with queues and n8n, an LLM router with Claude and RAG, and multi-tenant Postgres with row-level security and field-level encryption."/>

I design systems end to end, from the data model to the deploy pipeline. Patterns I use in production:

- **Multi-tenant SaaS**: shared schema with tenant keys, Postgres row-level security and cross-tenant tests in CI
- **BFF authentication**: httpOnly cookie sessions with token refresh owned in one place
- **Field-level encryption** for sensitive personal data, with key rotation and idempotent backfills
- **Event-driven pipelines**: webhooks, job queues, retries and idempotency keys
- **Edge compute**: Cloudflare Workers for payment links, SMS and API glue between voice agents and Stripe
- **LLM routing**: small models first, frontier models only when needed, prompt caching to cut token spend
- **Delivery**: Docker, Kubernetes + NGINX, Prometheus, and end-to-end tests that run against real data, not just mocks

## Tech stack

<img src="assets/stack.svg" width="100%" alt="Tech stack: Claude, Claude Code, MCP, Anthropic, OpenAI, Codex, Gemini, DeepSeek, OpenRouter, LangChain, Hugging Face, n8n, NotebookLM, Vapi, Twilio, ElevenLabs, Deepgram, Retell AI, Python, PyTorch, scikit-learn, LightGBM, XGBoost, ONNX, NumPy, pandas, Jupyter, OpenCV, Google Colab, Node.js, NestJS, FastAPI, Flask, Express, Prisma, Drizzle, PostgreSQL, Neon, MySQL, SQLite, MongoDB, Stripe, Resend, TypeScript, JavaScript, React, Next.js, Vite, Tailwind CSS, Astro, Streamlit, better-auth, C++, Docker, Kubernetes, NGINX, Prometheus, GitHub Actions, GHCR, Cloudflare, Cloudflare Workers, Vercel, MinIO, Linux, Bash, pnpm, Playwright, Jest, DrissionPage, Slack, Notion."/>

## Live GitHub stats

<img src="https://raw.githubusercontent.com/intikhab49/intikhab49/output/stats.svg" width="100%" alt="Live GitHub stats painted as a truck dashboard: contributions in the last 12 months on an odometer, public repos, stars and longest streak on gauges, and the weekly contributions drawn as a mountain range with a truck driving the ridge."/>

<sub>Redrawn every day by this repo's own GitHub Action. No third-party stats service.</sub>

## Work with me

I take on **contract and freelance work**:

- **AI voice agents**: receptionists, outbound callers, call-to-CRM and payment flows on Vapi and Twilio
- **RAG chatbots and LLM agents**: knowledge bases, tool calling, memory and evaluation
- **LLM cost and quality**: benchmarks, calibration, prompt caching and model routing
- **System architecture**: multi-tenant SaaS design, auth and data security, scaling and cost reviews
- **Agentic coding setups**: Claude Code skills, MCP servers and CI gates for AI-written code
- **Automation**: n8n workflows, lead generation, scraping, CRM and payment integrations
- **Microsoft gov cloud**: GCC, GCC High and Azure Government feature, endpoint and sign-in checks before you build
- **Make.com and no-code QA**: regression tests for Make scenarios that run offline and in CI

<a href="https://x.com/AzamIntikhab"><img src="assets/cta.svg" width="100%" alt="Open to contract work: voice AI agents, RAG, LLM evals, multi-tenant SaaS and automation. Message @AzamIntikhab on X. Horn do, rasta lo: honk, and I'll make way."/></a>

<div align="center">
<sub>Every image on this page is hand-coded, animated SVG in the style of Pakistani truck art, drawn by <a href=".github/scripts/build_art.py">build_art.py</a>. <b>Dekh magar pyar se</b>: look, but with love.</sub>
<br/><br/>
<sub>AI engineer · machine learning engineer · LLM engineer · AI researcher · systems architect · voice AI agent developer · Vapi · Twilio · RAG · agentic RAG · LLM evaluation · calibration · Claude Code · MCP · multi-tenant SaaS · Python · PyTorch · FastAPI · NestJS · open-source developer tools · GCC High · Azure Government · Microsoft 365 GCC · Make.com · Integromat · PostgreSQL · pgvector · Bitnami alternative · Docker · GitHub Actions · MCP server · PDF parsing for RAG · remote AI engineer in Pakistan</sub>
</div>
