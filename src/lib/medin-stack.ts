/**
 * Captions and stack extracted from Cole Medin,
 * "The ONLY AI Tech Stack You Need in 2026"
 * Full video: https://www.youtube.com/watch?v=21_k2St8bBI (34:25)
 * Short: https://www.youtube.com/shorts/wDTIQYxB71U
 * Diagram: https://drive.google.com/file/d/1diaAN6noQdnGRAW1B5vihBid_OUF4Isl/view
 *
 * Quotes below are from the auto-generated captions / on-screen list.
 */
export const MEDIN_VIDEO = {
  title: "The ONLY AI Tech Stack You Need in 2026",
  creator: "Cole Medin",
  url: "https://www.youtube.com/watch?v=21_k2St8bBI",
  shortUrl: "https://www.youtube.com/shorts/wDTIQYxB71U",
  duration: "34:25",
  published: "2025-11-05",
  chapters: [
    { t: "00:00", title: "Overview of my AI-First Tech Stack" },
    { t: "02:28", title: "The Core of the Tech Stack" },
    { t: "06:47", title: "The Core Stack for my AI Agents" },
    { t: "12:08", title: "Tools for RAG Agents" },
    { t: "18:44", title: "Tools for Web Automation Agents" },
    { t: "21:55", title: "My Full Stack App Dev Tech Stack" },
    { t: "27:03", title: "Tools/Platforms for Deployment & Infra" },
    { t: "32:11", title: "Other Self-Hostable Tools" },
    { t: "33:27", title: "Final Thoughts" },
  ],
  captions: [
    "So if you're looking to build any software going into 2026, listen up cuz I got some really solid recommendations for you.",
    "My tech stack is AI-first cuz I really don't see another way to do it these days.",
    "And I've been using pretty much the same tech stack except for some of the newer technologies for over a year now. So it doesn't change often. It is very stable. And I consider this a good thing.",
    "So for my database, most of the time I am using Postgres and I'm either using it through Neon or Superbase generally. So they are both platforms that host Postgres under the hood and I've been using Superbase for longer but experimenting with Neon more recently especially because of their scalability.",
    "And so with that, that'll take us into the next category here for the tools that I'm using for all of the AI agents that I create.",
    "Now, for my AI agent framework, right now, I'm pretty much exclusively using Pydantic AI, which people ask me why all of the time because there are so many good alternatives, even using no framework at all.",
    "But N8N for me is where it's at, and I feel like it's going to be like that long term. It is a phenomenal platform that I've covered so much on my channel, building things like rag agents.",
    "There are some good alternatives like Langflow and Flowise.",
  ],
};

export type StackNode = {
  id: string;
  name: string;
  layer:
    | "core"
    | "agents"
    | "rag"
    | "automation"
    | "fullstack"
    | "deploy"
    | "selfhost";
  role: string;
  why: string;
  alts: string[];
  nextlaw: string;
  oss: boolean;
};

export const STACK: StackNode[] = [
  {
    id: "postgres",
    name: "PostgreSQL (Neon / Supabase)",
    layer: "core",
    role: "System of record + pgvector memory",
    why: "Cole: 'OSS database for everything (RAG too). Scales extremely well. Easy hosting with Supabase/Neon. Open source and self-hostable.' He has used Supabase longer, Neon more recently for scalability.",
    alts: ["SQLite for local", "PGLite in preview"],
    nextlaw:
      "Matter memory, brief embeddings, and citation chunks. Preview uses local persistence; production maps onto Postgres + pgvector.",
    oss: true,
  },
  {
    id: "redis",
    name: "Redis / Valkey",
    layer: "core",
    role: "Cache, rate-limit, job queue",
    why: "Cole: Redis for caching; Valkey is the compatible OSS alternative. Open source and self-hostable.",
    alts: ["Valkey"],
    nextlaw: "Docket-watch debounce and CourtListener rate-limit shield.",
    oss: true,
  },
  {
    id: "claude-code",
    name: "Claude Code",
    layer: "core",
    role: "AI coding assistant",
    why: "Cole: 'Best current AI coding assistant. Slash commands, subagents, SKILLS. Very AI focused.'",
    alts: ["Codex", "Cursor"],
    nextlaw:
      "Persona skills in /playbook are the legal equivalent of Claude Code skills — trigger, mandate, steps, authorities.",
    oss: false,
  },
  {
    id: "n8n",
    name: "n8n",
    layer: "core",
    role: "Prototyping + background orchestration",
    why: "Cole: 'N8N for me is where it's at, and I feel like it's going to be like that long term. Hundreds of app integrations, fast.' Alternatives: Langflow, Flowise. Archon for RAG + task management.",
    alts: ["Langflow", "Flowise", "Archon"],
    nextlaw:
      "Intake webhooks, docket tracking, and multi-agent state delegation sit in this slot. The in-app triad is the interactive equivalent.",
    oss: true,
  },
  {
    id: "fastapi",
    name: "FastAPI",
    layer: "core",
    role: "API framework",
    why: "Cole: 'Everything you need for APIs. Async by default. Self-documenting.'",
    alts: ["Express", "TanStack Start server fns"],
    nextlaw:
      "This terminal's server functions (CourtListener, NY Senate, Grok triad, TTS) occupy the FastAPI slot on a TypeScript runtime.",
    oss: true,
  },
  {
    id: "pydantic-ai",
    name: "Pydantic AI",
    layer: "agents",
    role: "Single-agent framework",
    why: "Cole: 'Pretty much exclusively using Pydantic AI.' Flexibility and control, still easy, constant support for new protocols (MCP, AG-UI, A2A, Temporal). Alternatives: Agno, LlamaIndex, LangChain, or no framework.",
    alts: ["Agno", "LlamaIndex", "LangChain"],
    nextlaw: "Each of Planner, Executor, Critic is a typed agent with a structured JSON contract.",
    oss: true,
  },
  {
    id: "langgraph",
    name: "LangGraph",
    layer: "agents",
    role: "Multi-agent orchestration",
    why: "Cole: 'Everything I want for multi-agent: state management, human in the loop, node routing, graph persistence, UI. Integrations with every agent framework.' Alternatives: CrewAI, AutoGen, LlamaIndex workflows.",
    alts: ["CrewAI", "Microsoft AutoGen", "LlamaIndex workflows"],
    nextlaw:
      "Planner → Executor → Critic is a graph with a human-in-the-loop rewrite gate when critic score < 85.",
    oss: true,
  },
  {
    id: "arcade",
    name: "Arcade",
    layer: "agents",
    role: "Agent authorization / secure MCP",
    why: "Cole: 'Agent authorization — very underrated. Build auth-first MCP servers. MCP servers that are actually secure. All easy to work with.' Plus MCP Server SDK.",
    alts: ["Custom MCP auth"],
    nextlaw:
      "CourtListener MCP gateway is treated as an authenticated tool boundary. Tokens stay on the server.",
    oss: true,
  },
  {
    id: "langsmith",
    name: "LangSmith",
    layer: "agents",
    role: "Observability",
    why: "Cole: very feature rich; OSS alternatives Langfuse, Langwatch, Arize, Langtrace — open source and self-hostable.",
    alts: ["Langfuse", "Langwatch", "Arize", "Langtrace"],
    nextlaw: "Each triad run stores planner memo, draft, critic score, and unverified-cite list locally.",
    oss: false,
  },
  {
    id: "docling",
    name: "IBM Docling",
    layer: "rag",
    role: "File extraction + hybrid chunking",
    why: "Cole: 'Handles complex document extraction. Easy to use self-hosted models. Hybrid Chunking is insane. Integrates with many DBs.' Local, so briefs never need a closed OCR API.",
    alts: ["Unstructured", "LlamaParse"],
    nextlaw:
      "Local ingest on /research preserves heading hierarchy, markdown tables, and reading order from pasted briefs and text productions.",
    oss: true,
  },
  {
    id: "crawl4ai",
    name: "Crawl4AI",
    layer: "rag",
    role: "Website extraction",
    why: "Cole: 'FAST and efficient web crawling. Automatically cleans junk. LLM integrations. Scales very well.'",
    alts: ["Playwright + trafilatura"],
    nextlaw: "NY Senate + CourtListener connectors replace generic crawl for primary law.",
    oss: true,
  },
  {
    id: "pgvector",
    name: "pgvector",
    layer: "rag",
    role: "Vector store",
    why: "Cole's default: Postgres with pgvector so RAG and transactional data share one system of record.",
    alts: ["Qdrant"],
    nextlaw: "Citation and brief chunks keyed by matter id.",
    oss: true,
  },
  {
    id: "mem0",
    name: "Mem0",
    layer: "rag",
    role: "Long-term agent memory",
    why: "Cole recommends Mem0 for long-term memory across agent runs (client preferences, prior strategies).",
    alts: ["Zep", "custom table"],
    nextlaw: "Matter memory in the local store: facts, objectives, prior critic notes.",
    oss: true,
  },
  {
    id: "graphiti",
    name: "Neo4j + Graphiti",
    layer: "rag",
    role: "Knowledge graph",
    why: "Cole: Neo4j and Graphiti for knowledge graphs over entities, citations, and temporal facts.",
    alts: ["Memgraph"],
    nextlaw: "Citation network: statute → binding case → later citing cases (CourtListener opinions-cited).",
    oss: true,
  },
  {
    id: "ragas",
    name: "Ragas",
    layer: "rag",
    role: "RAG evaluation",
    why: "Cole uses Ragas to evaluate retrieval quality so the agent does not quietly cite junk.",
    alts: ["DeepEval"],
    nextlaw: "Critic Agent is the legal Ragas: verified vs unverified citation ratio is the eval metric.",
    oss: true,
  },
  {
    id: "playwright",
    name: "Playwright",
    layer: "automation",
    role: "Web automation",
    why: "Cole: Crawl4AI + Playwright for web automation agents that must click, not just fetch.",
    alts: ["Puppeteer"],
    nextlaw: "Reserved for docket-portal pulls that have no API.",
    oss: true,
  },
  {
    id: "react-shadcn",
    name: "React + shadcn/ui + Tailwind",
    layer: "fullstack",
    role: "Operator UI",
    why: "Cole's full-stack app layer: FastAPI + React + shadcn/Tailwind. Streamlit for rapid prototyping only.",
    alts: ["Next.js", "Streamlit (proto)"],
    nextlaw: "This terminal: TanStack Start, React 19, Tailwind v4, Radix/shadcn primitives.",
    oss: true,
  },
  {
    id: "render",
    name: "Render",
    layer: "deploy",
    role: "App hosting",
    why: "Cole prefers Render for simplicity of deployment.",
    alts: ["Vercel (this app)", "Fly.io"],
    nextlaw: "Ships on the Grok App Builder / Vercel path.",
    oss: false,
  },
  {
    id: "runpod",
    name: "RunPod",
    layer: "deploy",
    role: "GPU workloads",
    why: "Cole: RunPod for GPU-intensive workloads (local models, Docling serving).",
    alts: ["Modal", "Together"],
    nextlaw: "Docling/heavy OCR would land here; the preview uses Grok for language and local ingest for text.",
    oss: false,
  },
  {
    id: "digitalocean",
    name: "DigitalOcean",
    layer: "deploy",
    role: "VMs / self-host perimeter",
    why: "Cole: DigitalOcean for managing virtual machines when something must live inside a perimeter.",
    alts: ["Hetzner"],
    nextlaw: "The sovereign $0/month posture: self-host n8n + Postgres + the MCP gateway on a single droplet.",
    oss: false,
  },
  {
    id: "docker",
    name: "Docker",
    layer: "deploy",
    role: "Containerization",
    why: "Cole: Docker is the standard for containerization across the stack.",
    alts: ["Podman"],
    nextlaw: "Local AI package pattern (n8n, Postgres, Ollama) when running off-cloud.",
    oss: true,
  },
  {
    id: "gha",
    name: "GitHub Actions",
    layer: "deploy",
    role: "CI/CD + dependency audit",
    why: "Cole uses GitHub Actions to productionize. NextLaw spec adds `safety check` and secret isolation.",
    alts: ["Woodpecker"],
    nextlaw: "Zero-bypass: COURTLISTENER_API_TOKEN, SUPABASE_KEY, model keys never live in the repo.",
    oss: true,
  },
  {
    id: "ollama",
    name: "Ollama + Open WebUI + Qdrant + SearXNG",
    layer: "selfhost",
    role: "Local AI package",
    why: "Cole's self-host kit (extended n8n starter): Ollama, Open WebUI, n8n, Supabase, Flowise, Qdrant, SearXNG. One compose file, $0/month.",
    alts: ["LM Studio"],
    nextlaw: "The $0/month General Counsel path: this UI against a local model when an API key is absent.",
    oss: true,
  },
];

export const LAYER_LABEL: Record<StackNode["layer"], string> = {
  core: "Core infrastructure",
  agents: "General AI agents",
  rag: "RAG agents",
  automation: "Web automation",
  fullstack: "Full-stack apps",
  deploy: "Deploy & infra",
  selfhost: "Self-hostable",
};
