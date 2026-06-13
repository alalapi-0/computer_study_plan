#!/usr/bin/env node
/**
 * Lightweight MCP workspace config checker.
 * Does not print sensitive values.
 */

const fs = require("fs");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");
const MCP_PATH = path.join(REPO_ROOT, ".cursor", "mcp.json");

const REQUIRED_SERVERS = [
  "chrome-devtools",
  "context7",
  "filesystem",
  "github",
  "playwright",
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
    trimmed.startsWith("~")
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

function main() {
  let exitCode = 0;
  const issues = [];

  console.log("MCP Config Check");
  console.log("================");
  console.log(`Repo root: ${REPO_ROOT}`);
  console.log(`Config path: ${MCP_PATH}`);
  console.log("");

  if (!fs.existsSync(MCP_PATH)) {
    console.error("FAIL: .cursor/mcp.json does not exist.");
    process.exit(1);
  }

  let raw;
  try {
    raw = fs.readFileSync(MCP_PATH, "utf8");
  } catch (err) {
    console.error(`FAIL: cannot read config: ${err.message}`);
    process.exit(1);
  }

  let config;
  try {
    config = JSON.parse(raw);
  } catch (err) {
    console.error(`FAIL: invalid JSON: ${err.message}`);
    process.exit(1);
  }

  console.log("OK: JSON parsed successfully.");
  console.log("");

  const servers = config.mcpServers || {};
  const present = REQUIRED_SERVERS.filter((name) => Object.prototype.hasOwnProperty.call(servers, name));
  const missing = REQUIRED_SERVERS.filter((name) => !Object.prototype.hasOwnProperty.call(servers, name));

  console.log("Required servers:");
  for (const name of REQUIRED_SERVERS) {
    const status = servers[name] ? "present" : "MISSING";
    console.log(`  - ${name}: ${status}`);
  }
  console.log("");

  if (missing.length > 0) {
    issues.push(`Missing servers: ${missing.join(", ")}`);
    exitCode = 1;
  }

  const fsArgs = collectFilesystemArgs(config);
  if (fsArgs.length === 0) {
    issues.push("filesystem server has no authorized path argument.");
    exitCode = 1;
  } else {
    console.log("Filesystem authorized paths:");
    for (const arg of fsArgs) {
      const dangerous = isDangerousPath(arg);
      console.log(`  - ${arg}${dangerous ? " [DANGEROUS]" : ""}`);
      if (dangerous) {
        issues.push(`Dangerous filesystem path: ${arg}`);
        exitCode = 1;
      }
    }
    console.log("");
  }

  const envEntries = collectEnvEntries(config);
  if (envEntries.length > 0) {
    console.log("Environment variable references:");
    for (const entry of envEntries) {
      const suspicious = looksLikeRealToken(entry.value);
      console.log(
        `  - ${entry.server}.${entry.key}: ${suspicious ? "SUSPICIOUS (possible real token)" : "placeholder/reference"}`
      );
      if (suspicious) {
        issues.push(`Possible real token in ${entry.server}.env.${entry.key}`);
        exitCode = 1;
      }
    }
    console.log("");
  }

  console.log("Server summary:");
  for (const name of REQUIRED_SERVERS) {
    console.log(`  - ${name}: ${summarizeServer(servers[name])}`);
  }
  console.log("");

  if (issues.length > 0) {
    console.log("Issues:");
    for (const issue of issues) {
      console.log(`  - ${issue}`);
    }
    console.log("");
    process.exit(exitCode);
  }

  console.log("All checks passed.");
  process.exit(0);
}

main();
