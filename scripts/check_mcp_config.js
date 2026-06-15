#!/usr/bin/env node
/**
 * MCP config checker: project filesystem + Cursor Home global servers.
 * Does not print sensitive values.
 */

const fs = require("fs");
const os = require("os");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");
const PROJECT_MCP_PATH = path.join(REPO_ROOT, ".cursor", "mcp.json");
const GLOBAL_MCP_PATH = path.join(os.homedir(), ".cursor", "mcp.json");

const PROJECT_REQUIRED_SERVERS = ["filesystem"];
const GLOBAL_REQUIRED_SERVERS = [
  "chrome-devtools",
  "context7",
  "github",
  "playwright",
  "stitch",
];

const DANGEROUS_PATH_PATTERNS = [
  /^\/$/,
  /^~$/,
  /^~\/$/,
  /^\/Users\/[^/]+\/?$/,
  /^\/Volumes\/?$/,
  /^\/Volumes\/[^/]+\/?$/,
  /^C:\\$/,
  /^C:\\Users\\[^\\]+\\?$/,
  /^\/home\/[^/]+\/?$/,
];

const TOKEN_PATTERNS = [
  /\bghp_[A-Za-z0-9]{20,}\b/,
  /\bgithub_pat_[A-Za-z0-9_]{20,}\b/,
  /\bgho_[A-Za-z0-9]{20,}\b/,
  /\bghu_[A-Za-z0-9]{20,}\b/,
  /\bghs_[A-Za-z0-9]{20,}\b/,
  /\bghr_[A-Za-z0-9]{20,}\b/,
  /\bsk-[A-Za-z0-9]{20,}\b/,
  /\bAKIA[0-9A-Z]{16}\b/,
];

function isDangerousPath(value) {
  if (typeof value !== "string" || !value.trim()) return false;
  const normalized = value.trim();
  return DANGEROUS_PATH_PATTERNS.some((re) => re.test(normalized));
}

function looksLikeRealToken(value) {
  if (typeof value !== "string") return false;
  if (value.includes("${") && value.includes("}")) return false;
  return TOKEN_PATTERNS.some((re) => re.test(value));
}

function stripJsonComments(raw) {
  let out = "";
  let i = 0;
  while (i < raw.length) {
    if (raw[i] === '"') {
      out += raw[i];
      i += 1;
      while (i < raw.length) {
        out += raw[i];
        if (raw[i] === "\\") {
          i += 1;
          if (i < raw.length) {
            out += raw[i];
          }
        } else if (raw[i] === '"') {
          break;
        }
        i += 1;
      }
      i += 1;
      continue;
    }
    if (raw.startsWith("/*", i)) {
      const end = raw.indexOf("*/", i + 2);
      i = end === -1 ? raw.length : end + 2;
      continue;
    }
    if (raw.startsWith("//", i)) {
      const end = raw.indexOf("\n", i + 2);
      i = end === -1 ? raw.length : end + 1;
      continue;
    }
    out += raw[i];
    i += 1;
  }
  return out;
}

function readJsonConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    return { ok: false, error: "file does not exist", config: null };
  }
  try {
    const raw = fs.readFileSync(configPath, "utf8");
    const config = JSON.parse(stripJsonComments(raw));
    return { ok: true, config, error: null };
  } catch (err) {
    return { ok: false, error: err.message, config: null };
  }
}

function collectEnvEntries(config) {
  const entries = [];
  const servers = config.mcpServers || {};
  for (const [name, server] of Object.entries(servers)) {
    const env = server && server.env;
    if (!env || typeof env !== "object") continue;
    for (const [key, value] of Object.entries(env)) {
      entries.push({ server: name, key, value: String(value) });
    }
  }
  return entries;
}

function isPathLikeArg(value) {
  if (typeof value !== "string") return false;
  const trimmed = value.trim();
  if (!trimmed || trimmed.startsWith("-")) return false;
  if (trimmed.startsWith("@")) return false;
  return (
    trimmed === "." ||
    trimmed.startsWith("./") ||
    trimmed.startsWith("/") ||
    trimmed.startsWith("~") ||
    trimmed.includes("workspaceFolder")
  );
}

function collectFilesystemArgs(config) {
  const server = (config.mcpServers || {}).filesystem;
  if (!server || !Array.isArray(server.args)) return [];
  return server.args.filter(isPathLikeArg);
}

function summarizeServer(server) {
  if (!server || typeof server !== "object") return "(missing config)";
  const parts = [];
  if (server.command) parts.push(`command=${server.command}`);
  if (Array.isArray(server.args)) parts.push(`args=${server.args.length}`);
  if (server.env && typeof server.env === "object") {
    parts.push(`envKeys=${Object.keys(server.env).join(",")}`);
  }
  return parts.join(", ") || "(empty)";
}

function checkServerPresence(label, configPath, requiredServers, issues) {
  const result = readJsonConfig(configPath);
  console.log(`${label} config: ${configPath}`);

  if (!result.ok) {
    console.log(`  FAIL: ${result.error}`);
    issues.push(`${label}: ${result.error}`);
    return null;
  }

  console.log("  OK: JSON parsed successfully.");
  const servers = result.config.mcpServers || {};
  const missing = requiredServers.filter(
    (name) => !Object.prototype.hasOwnProperty.call(servers, name)
  );

  for (const name of requiredServers) {
    const status = servers[name] ? "present" : "MISSING";
    console.log(`  - ${name}: ${status}`);
  }

  if (missing.length > 0) {
    issues.push(`${label} missing servers: ${missing.join(", ")}`);
  }

  return { config: result.config, servers };
}

function main() {
  let exitCode = 0;
  const issues = [];

  console.log("MCP Config Check");
  console.log("================");
  console.log(`Repo root: ${REPO_ROOT}`);
  console.log("");

  const projectResult = checkServerPresence(
    "Project",
    PROJECT_MCP_PATH,
    PROJECT_REQUIRED_SERVERS,
    issues
  );
  console.log("");

  const globalResult = checkServerPresence(
    "Cursor Home",
    GLOBAL_MCP_PATH,
    GLOBAL_REQUIRED_SERVERS,
    issues
  );
  console.log("");

  if (projectResult) {
    const fsArgs = collectFilesystemArgs(projectResult.config);
    if (fsArgs.length === 0) {
      issues.push("filesystem server has no authorized path argument.");
    } else {
      console.log("Filesystem authorized paths:");
      for (const arg of fsArgs) {
        const dangerous = isDangerousPath(arg);
        console.log(`  - ${arg}${dangerous ? " [DANGEROUS]" : ""}`);
        if (dangerous) {
          issues.push(`Dangerous filesystem path: ${arg}`);
        }
      }
      console.log("");
    }

    const envEntries = collectEnvEntries(projectResult.config);
    if (envEntries.length > 0) {
      console.log("Project environment variable references:");
      for (const entry of envEntries) {
        const suspicious = looksLikeRealToken(entry.value);
        console.log(
          `  - ${entry.server}.${entry.key}: ${
            suspicious ? "SUSPICIOUS (possible real token)" : "placeholder/reference"
          }`
        );
        if (suspicious) {
          issues.push(`Possible real token in ${entry.server}.env.${entry.key}`);
        }
      }
      console.log("");
    }
  }

  if (globalResult) {
    const envEntries = collectEnvEntries(globalResult.config);
    if (envEntries.length > 0) {
      console.log("Cursor Home environment variable references:");
      for (const entry of envEntries) {
        const suspicious = looksLikeRealToken(entry.value);
        console.log(
          `  - ${entry.server}.${entry.key}: ${
            suspicious ? "WARN (possible real token in ~/.cursor/mcp.json)" : "placeholder/reference"
          }`
        );
        if (suspicious) {
          console.log(
            "    -> Prefer ${GITHUB_PERSONAL_ACCESS_TOKEN} placeholder in ~/.cursor/mcp.json; keep secrets in shell env only."
          );
        }
      }
      console.log("");
    }
  }

  console.log("Server summary:");
  if (projectResult) {
    for (const name of PROJECT_REQUIRED_SERVERS) {
      console.log(`  - ${name} (project): ${summarizeServer(projectResult.servers[name])}`);
    }
  }
  if (globalResult) {
    for (const name of GLOBAL_REQUIRED_SERVERS) {
      console.log(`  - ${name} (global): ${summarizeServer(globalResult.servers[name])}`);
    }
  }
  console.log("");

  if (issues.length > 0) {
    console.log("Issues:");
    for (const issue of issues) {
      console.log(`  - ${issue}`);
    }
    console.log("");
    process.exit(1);
  }

  console.log("All checks passed.");
  console.log(
    "NOTE: config PASS does not guarantee Cursor loaded MCP servers in the current Agent thread."
  );
  console.log("      Run npm run check:cursor-mcp and verify thread tools when needed.");
  process.exit(0);
}

main();
