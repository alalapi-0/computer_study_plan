// progress_ui.js — Web 写操作、阅读器、任务反馈与动作记录

let feedbackMap = {};
let eventMap = {};
let apiReady = false;
let terminalHistory = [];
let terminalCwd = "";
let terminalCwdDisplay = "~";
let terminalStateInfo = null;
let activeTerminalTaskId = "";
let workspaceTaskId = "";
let inlineReaderTaskId = "";
let inlineReaderFile = "";
let routeFocusedRound = false;
let autoBindingTerminalTaskId = "";

const TERMINAL_QUICK_COMMANDS = [
  "pwd",
  "ls",
  "ls -la",
  "find . -maxdepth 2 -type f",
];

async function detectApi() {
  if (window.location.protocol === "file:") {
    apiReady = false;
    return;
  }
  try {
    const res = await fetch("/api/health?_=" + Date.now());
    apiReady = res.ok;
  } catch (_) {
    apiReady = false;
  }
  const banner = document.getElementById("apiBanner");
  if (!banner) return;
  if (apiReady) {
    banner.className = "banner ok";
    banner.innerHTML = "";
    banner.style.display = "none";
  } else if (window.location.protocol !== "file:") {
    banner.className = "banner warn";
    banner.innerHTML =
      '<strong>只读模式</strong> — 请用 <code>python3 scripts/progress_server.py</code> 启动以启用网页记录。';
    banner.style.display = "block";
  } else {
    banner.className = "banner warn";
    banner.innerHTML =
      '<strong>本地文件模式</strong> — 建议运行 <code>python3 scripts/progress_server.py</code> 后访问 Web UI 学习工作区。';
    banner.style.display = "block";
  }
}

async function loadFeedbackData() {
  if (window.location.protocol === "file:") return;
  try {
    const res = await fetch("/api/feedback?_=" + Date.now());
    if (!res.ok) return;
    const data = await res.json();
    feedbackMap = data.feedback || {};
  } catch (_) {}
}

async function loadEventData() {
  if (window.location.protocol === "file:") return;
  try {
    const res = await fetch("/api/events?_=" + Date.now());
    if (!res.ok) return;
    const data = await res.json();
    eventMap = data.by_task || {};
  } catch (_) {}
}

async function postTaskAction(taskId, undo, payload) {
  if (!apiReady) {
    showToast("请先运行 python3 scripts/progress_server.py 启动服务", "warn");
    return null;
  }
  const action = undo ? "undo" : "done";
  const res = await fetch(`/api/tasks/${encodeURIComponent(taskId)}/${action}`, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload || {}),
  });
  const data = await res.json();
  if (!res.ok) {
    showToast(data.error || "操作失败", "error");
    return null;
  }
  progressData = data.tasks || progressData;
  lanesData = data.lanes || lanesData;
  feedbackMap = data.feedback || feedbackMap;
  await loadFeedbackData();
  await loadEventData();
  showToast(undo ? "已撤销完成" : "已保存记录并完成", "ok");
  render();
  return data;
}

function showToast(msg, kind) {
  let el = document.getElementById("toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    document.body.appendChild(el);
  }
  el.className = "toast " + (kind || "");
  el.textContent = msg;
  el.style.opacity = "1";
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.style.opacity = "0"; }, 2200);
}

function terminalPrompt(cwdDisplay) {
  return `${cwdDisplay || "~"} $`;
}

function terminalTaskContext() {
  if (!activeTerminalTaskId) return null;
  return taskMeta(activeTerminalTaskId);
}

function currentWorkspaceTask() {
  return typeof findNextTask === "function" ? findNextTask() : null;
}

function terminalCwdForRound(round) {
  const match = String(round?.id || "").match(/round_(\d{2})/);
  if (!match) return "~";
  return `~/cli-lab/round${Number(match[1])}`;
}

function terminalTaskTarget(taskId) {
  const meta = taskMeta(taskId);
  if (!meta) return "~";
  return terminalCwdForRound(meta.round);
}

function taskUsesTerminal(task) {
  if (!task) return false;
  const meta = taskMeta(task.id);
  if (meta?.round?.lane !== "linux-foundations") return false;
  return ["reading", "exercise", "test", "output"].includes(task.type);
}

function terminalQuickCommands() {
  const meta = terminalTaskContext();
  const commands = ["pwd", "ls", "ls -la"];
  const weekMatch = String(meta?.week?.id || "").match(/week(\d+)/);
  if (weekMatch) {
    const weekDir = `week${Number(weekMatch[1])}`;
    commands.push(`mkdir -p ${weekDir}/self_check`, `cd ${weekDir}/self_check`);
  }
  if (meta?.round?.id === "round_00" && meta?.week?.id?.includes("week1")) {
    commands.push("cd notes", "pwd", "cd ..");
  }
  commands.push("find . -maxdepth 2 -type f");
  return [...new Set(commands)];
}

function scrollWorkspacePanel(panelId) {
  const panel = document.getElementById(panelId);
  const workspace = document.getElementById("learnWorkspace");
  const mobile = window.matchMedia?.("(max-width: 760px)")?.matches;
  const target = mobile && panel ? panel : workspace;
  target?.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function autoBindTerminalForTask(taskId) {
  if (!apiReady || !taskId || activeTerminalTaskId || autoBindingTerminalTaskId === taskId) return;
  const meta = taskMeta(taskId);
  if (!meta || !taskUsesTerminal(meta.task)) return;
  autoBindingTerminalTaskId = taskId;
  activeTerminalTaskId = taskId;
  try {
    const target = terminalTaskTarget(taskId);
    const state = await setTerminalCwd(target);
    if (!terminalHistory.length) {
      terminalHistory.push({
        kind: "system",
        message: `已自动绑定当前任务：${meta.task.title}；工作目录 ${state?.cwd_display || target}`,
        cwd_display: state?.cwd_display || "~",
      });
    }
    renderTerminal();
  } catch (err) {
    activeTerminalTaskId = "";
    showToast(err.message || "终端自动绑定失败", "warn");
  } finally {
    autoBindingTerminalTaskId = "";
  }
}

function renderTerminalContext() {
  const contextEl = document.getElementById("terminalContext");
  const quickEl = document.getElementById("terminalQuickCommands");
  const cwdEl = document.getElementById("terminalCwd");
  const allowedEl = document.getElementById("terminalAllowed");
  if (cwdEl) cwdEl.textContent = terminalCwdDisplay || "~";
  if (allowedEl) {
    const allowed = terminalStateInfo?.allowed || [];
    allowedEl.textContent = allowed.length
      ? allowed.slice(0, 18).join(" ")
      : "等待连接";
  }
  if (quickEl) {
    quickEl.innerHTML = terminalQuickCommands().map((cmd) => (
      `<button type="button" class="terminal-chip" data-command="${escapeHtml(cmd)}">${escapeHtml(cmd)}</button>`
    )).join("");
    quickEl.querySelectorAll(".terminal-chip").forEach((btn) => {
      btn.addEventListener("click", () => runTerminalCommand(btn.getAttribute("data-command") || ""));
    });
  }
  if (!contextEl) return;
  const meta = terminalTaskContext();
  if (!meta) {
    const current = currentWorkspaceTask();
    if (current && !taskUsesTerminal(current.task)) {
      contextEl.innerHTML = `
      <div class="terminal-context-title">当前任务不需要终端</div>
      <div class="terminal-context-meta">${escapeHtml(current.task.title)} 属于 ${escapeHtml(current.round.lane)}，先读资料并写记录即可。</div>
    `;
      return;
    }
    contextEl.innerHTML = `
      <div class="terminal-context-title">未绑定任务</div>
      <div class="terminal-context-meta">打开工程任务时会自动绑定；任务行的“终端练习”用于切换或重新聚焦。</div>
    `;
    return;
  }
  const done = isTaskDone(meta.task.id);
  const canRead = canOpenFile(meta.task.file);
  contextEl.innerHTML = `
    <div class="terminal-context-title">${escapeHtml(meta.task.title)}</div>
    <div class="terminal-context-meta">${escapeHtml(meta.round.title)} / ${escapeHtml(meta.week.title)}</div>
    <div class="terminal-context-path">${escapeHtml(meta.task.file || "手动练习")}</div>
    <div class="terminal-context-actions">
      ${canRead ? `<button type="button" class="task-btn read task-open" data-task="${escapeHtml(meta.task.id)}" data-file="${escapeHtml(meta.task.file)}" data-title="${escapeHtml(meta.task.title)}">${fileActionLabel(meta.task.file, meta.task.type)}</button>` : ""}
      ${taskRecordButton(meta.task.id)}
      ${taskActionButtons(meta.task.id, done)}
    </div>
  `;
  bindTaskActions(contextEl);
}

function renderTerminal() {
  const output = document.getElementById("terminalOutput");
  const prompt = document.getElementById("terminalPrompt");
  if (!output || !prompt) return;
  const current = currentWorkspaceTask();
  const idleForCurrentTask = !activeTerminalTaskId && current && !taskUsesTerminal(current.task);
  document.getElementById("terminal")?.classList.toggle("terminal-idle", !!idleForCurrentTask);
  document.getElementById("learnWorkspace")?.classList.toggle("no-terminal-task", !!idleForCurrentTask);
  prompt.textContent = terminalPrompt(terminalCwdDisplay || "~");
  renderTerminalContext();
  if (!terminalHistory.length) {
    if (idleForCurrentTask) {
      output.innerHTML = `<div class="terminal-line muted">当前任务以阅读和记录为主，不需要终端。切到工程实操任务后，终端会自动绑定沙盒目录。</div>`;
      return;
    }
    output.innerHTML = `<div class="terminal-line muted">终端已映射到 <code>~/cli-lab</code> 沙盒。工程任务会自动绑定到对应 Round 目录。</div>`;
    return;
  }
  output.innerHTML = terminalHistory.map((entry) => {
    if (entry.kind === "system") {
      return `<div class="terminal-entry system"><div class="terminal-command">${escapeHtml(entry.message)}</div></div>`;
    }
    if (entry.kind === "error") {
      return `<div class="terminal-entry"><div class="terminal-command">${escapeHtml(entry.prompt)} ${escapeHtml(entry.command)}</div><pre class="terminal-stderr">${escapeHtml(entry.error)}</pre></div>`;
    }
    const stdout = entry.stdout ? `<pre>${escapeHtml(entry.stdout)}</pre>` : "";
    const stderr = entry.stderr ? `<pre class="terminal-stderr">${escapeHtml(entry.stderr)}</pre>` : "";
    const status = entry.result && entry.result !== "ok" ? `<span class="terminal-result ${escapeHtml(entry.result)}">${escapeHtml(entry.result)}</span>` : "";
    return `<div class="terminal-entry"><div class="terminal-command">${escapeHtml(entry.prompt)} ${escapeHtml(entry.command)} ${status}</div>${stdout}${stderr}</div>`;
  }).join("");
  output.scrollTop = output.scrollHeight;
}

async function loadTerminalState() {
  const input = document.getElementById("terminalInput");
  if (!apiReady) {
    terminalHistory = [{ kind: "error", prompt: "~ $", command: "", error: "请用 python3 scripts/progress_server.py 启动后使用终端练习。", cwd_display: "~" }];
    renderTerminal();
    if (input) input.disabled = true;
    return;
  }
  if (input) input.disabled = false;
  try {
    const requestedCwd = terminalCwd || (activeTerminalTaskId ? terminalTaskTarget(activeTerminalTaskId) : "");
    const res = await fetch(`/api/terminal?cwd=${encodeURIComponent(requestedCwd)}&_=${Date.now()}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "terminal_state_failed");
    terminalStateInfo = data.terminal || null;
    terminalCwd = data.terminal.cwd || "";
    terminalCwdDisplay = data.terminal.cwd_display || "~";
    renderTerminal();
  } catch (err) {
    terminalHistory.push({ kind: "error", prompt: "~ $", command: "", error: err.message, cwd_display: "~" });
    renderTerminal();
  }
}

async function setTerminalCwd(cwd) {
  if (!apiReady) {
    showToast("请先运行 python3 scripts/progress_server.py 启动服务", "warn");
    return null;
  }
  const res = await fetch(`/api/terminal?cwd=${encodeURIComponent(cwd || "")}&_=${Date.now()}`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "terminal_state_failed");
  terminalStateInfo = data.terminal || null;
  terminalCwd = data.terminal.cwd || "";
  terminalCwdDisplay = data.terminal.cwd_display || "~";
  renderTerminal();
  return data.terminal;
}

async function openTaskTerminal(taskId) {
  if (!apiReady) {
    showToast("请先运行 python3 scripts/progress_server.py 启动服务", "warn");
    return;
  }
  const meta = taskMeta(taskId);
  if (!meta) return;
  workspaceTaskId = taskId;
  activeTerminalTaskId = taskId;
  try {
    const target = terminalTaskTarget(taskId);
    const state = await setTerminalCwd(target);
    terminalHistory.push({
      kind: "system",
      message: `已绑定任务：${meta.task.title}；工作目录 ${state?.cwd_display || target}`,
      cwd_display: state?.cwd_display || "~",
    });
    renderTerminal();
    if (canOpenFile(meta.task.file)) {
      await openInlineReader(meta.task.file, meta.task.title, taskId, { silent: true });
    }
    renderContinue();
    scrollWorkspacePanel("terminal");
    setTimeout(() => document.getElementById("terminalInput")?.focus({ preventScroll: true }), 220);
  } catch (err) {
    showToast(err.message || "终端切换失败", "error");
  }
}

async function runTerminalCommand(command) {
  if (!apiReady) {
    showToast("请先运行 python3 scripts/progress_server.py 启动服务", "warn");
    return;
  }
  const value = String(command || "").trim();
  if (!value) return;
  const input = document.getElementById("terminalInput");
  if (input) input.disabled = true;
  const currentPrompt = document.getElementById("terminalPrompt")?.textContent || "~ $";
  try {
    const res = await fetch("/api/terminal/run", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ command: value, cwd: terminalCwd, task_id: activeTerminalTaskId }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "terminal_run_failed");
    const term = data.terminal || {};
    terminalCwd = term.cwd || terminalCwd;
    terminalCwdDisplay = term.cwd_display || terminalCwdDisplay;
    if (term.clear) {
      terminalHistory = [];
    } else {
      terminalHistory.push({
        command: value,
        prompt: currentPrompt,
        result: term.result || "ok",
        returncode: term.returncode,
        stdout: term.stdout || "",
        stderr: term.stderr || "",
        cwd_display: term.cwd_display || "~",
      });
    }
    renderTerminal();
  } catch (err) {
    terminalHistory.push({
      kind: "error",
      command: value,
      prompt: currentPrompt,
      error: err.message,
      cwd_display: terminalCwdDisplay || "~",
    });
    renderTerminal();
    showToast("命令被拦截或执行失败", "warn");
  } finally {
    if (input) {
      input.disabled = false;
      input.value = "";
      input.focus();
    }
  }
}

async function resetTerminal() {
  activeTerminalTaskId = "";
  terminalCwd = "";
  try {
    const state = await setTerminalCwd("~/cli-lab");
    terminalHistory.push({
      kind: "system",
      message: `已回到 ${state?.cwd_display || "~/cli-lab"} 根目录`,
      cwd_display: state?.cwd_display || "~/cli-lab",
    });
    renderTerminal();
    document.getElementById("terminalInput")?.focus({ preventScroll: true });
  } catch (err) {
    showToast(err.message || "终端重置失败", "warn");
  }
}

function feedbackFor(taskId) {
  return feedbackMap[taskId] || null;
}

function eventsFor(taskId) {
  return eventMap[taskId] || [];
}

function renderFeedbackHint(taskId) {
  const fb = feedbackFor(taskId);
  if (!fb || fb.feedback_type === "completed") return "";
  const text = fb.next_suggestion || fb.message || "";
  if (!text) return "";
  return `<div class="task-feedback">${escapeHtml(text)}</div>`;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function taskActionButtons(taskId, done) {
  if (!apiReady) return "";
  if (done) {
    return `<button type="button" class="task-btn undo" data-task="${taskId}" data-action="undo">撤销</button>`;
  }
  return `<button type="button" class="task-btn done task-complete-open" data-task="${taskId}">记录并完成</button>`;
}

function fileActionLabel(filePath, taskType) {
  const file = String(filePath || "");
  if (/\.(sh|py)$/i.test(file)) return "查看脚本";
  if (taskType === "reading" || /\.md$/i.test(file)) return "读教程";
  return "打开资料";
}

function taskRecordButton(taskId) {
  if (!apiReady) return "";
  if (!isTaskDone(taskId)) return "";
  const count = eventsFor(taskId).length;
  const label = count ? `记录 ${count}` : "记录";
  return `<button type="button" class="task-btn record task-record-open" data-task="${taskId}">${label}</button>`;
}

function isRunnableTask(task) {
  return !!(task && /\.(sh|py)$/i.test(task.file || "") && task.type === "exercise");
}

function taskRunButton(task) {
  if (!apiReady || !isRunnableTask(task)) return "";
  return `<button type="button" class="task-btn run task-run" data-task="${task.id}">运行脚本</button>`;
}

function taskTerminalButton(task) {
  if (!apiReady || !taskUsesTerminal(task)) return "";
  return `<button type="button" class="task-btn terminal task-terminal" data-task="${task.id}">终端练习</button>`;
}

async function postTaskRun(taskId) {
  if (!apiReady) {
    showToast("请先运行 python3 scripts/progress_server.py 启动服务", "warn");
    return null;
  }
  const meta = taskMeta(taskId);
  const file = meta?.task?.file || "";
  const title = meta?.task?.title || taskId;
  const roundId = meta?.round?.id || "";
  const roundMatch = roundId.match(/round_(\d{2})/);
  const sandbox = roundMatch
    ? `~/cli-lab/round${Number(roundMatch[1])}`
    : "~/cli-lab";
  const ok = window.confirm(
    `将在本地沙盒执行白名单练习脚本：\n${file}\n\n工作目录：${sandbox}\n脚本可能写入沙盒、调用完成记录脚本并追加动作记录。继续？`
  );
  if (!ok) return null;

  const res = await fetch(`/api/tasks/${encodeURIComponent(taskId)}/run`, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  });
  const data = await res.json();
  if (!res.ok) {
    showToast(data.error || "运行失败", "error");
    return null;
  }
  progressData = data.tasks || progressData;
  lanesData = data.lanes || lanesData;
  feedbackMap = data.feedback || feedbackMap;
  await loadFeedbackData();
  await loadEventData();
  render();
  openExecutionResult(title, data.execution || {});
  const result = data.execution?.result || "";
  showToast(result === "ok" ? "练习脚本运行完成" : "练习脚本已结束，请查看输出", result === "ok" ? "ok" : "warn");
  return data;
}

function bindTaskActions(container) {
  container.querySelectorAll(".task-btn[data-action]").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.getAttribute("data-task");
      const undo = btn.getAttribute("data-action") === "undo";
      btn.disabled = true;
      await postTaskAction(id, undo);
      btn.disabled = false;
    });
  });
  container.querySelectorAll(".task-record-open").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      openRecordViewer(btn.getAttribute("data-task"));
    });
  });
  container.querySelectorAll(".task-complete-open").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      openRecordViewer(btn.getAttribute("data-task"), { requireNote: true });
    });
  });
  container.querySelectorAll(".task-run").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.getAttribute("data-task");
      btn.disabled = true;
      await postTaskRun(id);
      btn.disabled = false;
    });
  });
  container.querySelectorAll(".task-terminal").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      btn.disabled = true;
      await openTaskTerminal(btn.getAttribute("data-task"));
      btn.disabled = false;
    });
  });
  container.querySelectorAll(".task-open").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      openInlineReader(
        btn.getAttribute("data-file"),
        btn.getAttribute("data-title") || "阅读",
        btn.getAttribute("data-task") || "",
      );
    });
  });
}

async function openInlineReader(filePath, title, taskId, options) {
  if (!filePath) return;
  const body = document.getElementById("inlineReaderBody");
  const heading = document.getElementById("inlineReaderTitle");
  const metaEl = document.getElementById("inlineReaderMeta");
  const popout = document.getElementById("inlineReaderPopout");
  if (!body || !heading) {
    openMarkdownViewer(filePath, title);
    return;
  }
  if (taskId) workspaceTaskId = taskId;
  inlineReaderTaskId = taskId || inlineReaderTaskId;
  inlineReaderFile = filePath;
  heading.textContent = title || filePath;
  if (metaEl) metaEl.textContent = filePath;
  if (popout) {
    popout.disabled = false;
    popout.dataset.file = filePath;
    popout.dataset.title = title || filePath;
  }
  body.innerHTML = "<p class='reader-loading'>加载中…</p>";
  if (!options?.silent) {
    scrollWorkspacePanel("inlineReaderPanel");
  }
  try {
    const resourcePath = "/" + filePath.replace(/^\//, "");
    const separator = resourcePath.includes("?") ? "&" : "?";
    const res = await fetch(`${resourcePath}${separator}_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    body.innerHTML = /\.(sh|py|js|json)$/i.test(filePath)
      ? renderCodeDocument(text, filePath)
      : renderMarkdown(text, filePath);
    bindReaderDocumentLinks(body);
  } catch (err) {
    body.innerHTML = `<p class='reader-error'>无法加载 ${escapeHtml(filePath)}：${escapeHtml(err.message)}</p>`;
  }
}

async function openMarkdownViewer(filePath, title) {
  if (!filePath) return;
  const modal = document.getElementById("readerModal");
  const body = document.getElementById("readerBody");
  const heading = document.getElementById("readerTitle");
  if (!modal || !body) return;
  heading.textContent = title || filePath;
  body.innerHTML = "<p class='reader-loading'>加载中…</p>";
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  try {
    const resourcePath = "/" + filePath.replace(/^\//, "");
    const separator = resourcePath.includes("?") ? "&" : "?";
    const res = await fetch(`${resourcePath}${separator}_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    if (/\.(sh|py|js|json)$/i.test(filePath)) {
      body.innerHTML = renderCodeDocument(text, filePath);
    } else {
      body.innerHTML = renderMarkdown(text, filePath);
    }
    bindReaderDocumentLinks(body);
  } catch (err) {
    body.innerHTML = `<p class='reader-error'>无法加载 ${escapeHtml(filePath)}：${escapeHtml(err.message)}</p>`;
  }
}

function taskMeta(taskId) {
  for (const round of ROUNDS || []) {
    for (const week of round.weeks || []) {
      const task = (week.tasks || []).find((item) => item.id === taskId);
      if (task) return { round, week, task };
    }
  }
  return null;
}

function openRecordViewer(taskId, options = {}) {
  const modal = document.getElementById("readerModal");
  const body = document.getElementById("readerBody");
  const heading = document.getElementById("readerTitle");
  if (!modal || !body || !heading) return;

  const meta = taskMeta(taskId);
  const title = meta?.task?.title || taskId;
  const done = isTaskDone(taskId);
  const fb = feedbackFor(taskId);
  const events = eventsFor(taskId).slice().reverse();

  heading.textContent = `学习记录 · ${title}`;
  body.innerHTML = renderRecordBody(taskId, done, fb, events, options, meta);
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");

  const saveBtn = body.querySelector("#recordSaveDone");
  const undoBtn = body.querySelector("#recordUndoDone");
  const action = async (undo) => {
    const note = body.querySelector("#recordNote")?.value.trim() || "";
    const evidencePath = body.querySelector("#recordEvidence")?.value || "";
    const btn = undo ? undoBtn : saveBtn;
    if (!undo && (options.requireNote || !done) && !note) {
      showToast("请先写一条本次记录，再保存完成", "warn");
      body.querySelector("#recordNote")?.focus();
      return;
    }
    if (btn) btn.disabled = true;
    await postTaskAction(taskId, undo, { note, evidence_path: evidencePath });
    closeMarkdownViewer();
  };
  if (saveBtn) saveBtn.addEventListener("click", () => action(false));
  if (undoBtn) undoBtn.addEventListener("click", () => action(true));
}

function recordPlaceholders(meta, taskId) {
  const lane = meta?.round?.lane || taskLane(taskId);
  const file = meta?.task?.file || "";
  if (lane === "linux-foundations") {
    const match = String(meta?.round?.id || "").match(/round_(\d{2})/);
    const roundPath = match ? `~/cli-lab/round${Number(match[1])}` : "~/cli-lab";
    return {
      note: "例如：读完本节 Linux 笔记，并在终端完成 1 个最小验证；下一步继续做本周练习。",
      evidence: `例如：${roundPath}/week1_auto`,
    };
  }
  return {
    note: "例如：读完当前 Linux 资料，整理一个最小结论，并写清下一步。",
    evidence: file ? `例如：${file}` : "例如：records/weekly_reviews/YYYY-WW.md",
  };
}

function exampleText(text) {
  return String(text || "").replace(/^例如：/, "");
}

function renderRecordBody(taskId, done, fb, events, options = {}, meta = null) {
  const placeholders = recordPlaceholders(meta, taskId);
  const suggestion = fb?.next_suggestion || "";
  const eventRows = events.length
    ? events.slice(0, 12).map((event) => `
        <li>
          <strong>${escapeHtml(actionLabel(event.action_type))}</strong>
          <span>${escapeHtml(event.timestamp || "")}</span>
          ${event.note ? `<p>${escapeHtml(event.note)}</p>` : ""}
          ${event.evidence_path ? `<code>${escapeHtml(event.evidence_path)}</code>` : ""}
        </li>
      `).join("")
    : "<li class='record-empty'>还没有动作记录。</li>";

  return `
    <div class="record-panel">
      <div class="record-status ${done ? "done" : "open"}">${done ? "当前状态：已完成" : "当前状态：未完成"}</div>
      <p>${escapeHtml(fb?.message || "暂无反馈。")}</p>
      ${suggestion ? `<p class="record-suggestion">${escapeHtml(suggestion)}</p>` : ""}
      <div class="record-template">
        <strong>记录参考</strong>
        <p>${escapeHtml(exampleText(placeholders.note))}</p>
        <p>证据示例：<code>${escapeHtml(exampleText(placeholders.evidence))}</code></p>
      </div>
      <label class="record-label">本次记录${done && !options.requireNote ? "（建议填写）" : "（必填）"}</label>
      <textarea id="recordNote" class="record-input" placeholder="${escapeHtml(placeholders.note)}"></textarea>
      <label class="record-label">证据路径（可选）</label>
      <input id="recordEvidence" class="record-input" placeholder="${escapeHtml(placeholders.evidence)}" />
      <div class="record-actions">
        <button type="button" class="task-btn done" id="recordSaveDone">${done ? "保存记录并保持完成" : "记录并完成"}</button>
        ${done ? '<button type="button" class="task-btn undo" id="recordUndoDone">撤销完成</button>' : ""}
      </div>
      <h4>最近记录</h4>
      <ul class="record-list">${eventRows}</ul>
    </div>
  `;
}

function actionLabel(actionType) {
  if (actionType === "mark_done") return "记录并完成";
  if (actionType === "undo_done") return "撤销完成";
  if (actionType === "run_exercise") return "运行脚本";
  return actionType || "动作";
}

function openExecutionResult(title, execution) {
  const modal = document.getElementById("readerModal");
  const body = document.getElementById("readerBody");
  const heading = document.getElementById("readerTitle");
  if (!modal || !body || !heading) return;
  heading.textContent = `运行结果 · ${title}`;
  body.innerHTML = renderExecutionResult(execution);
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function renderExecutionResult(execution) {
  const result = execution.result || "unknown";
  const statusText = {
    ok: "运行成功",
    failed: "脚本返回非零状态",
    timeout: "运行超时，已停止",
  }[result] || "运行结束";
  const stdout = execution.stdout || "";
  const stderr = execution.stderr || "";
  return `
    <div class="run-panel">
      <div class="run-status ${escapeHtml(result)}">${escapeHtml(statusText)}</div>
      <div class="run-meta">
        <span>脚本：<code>${escapeHtml(execution.script_path || "")}</code></span>
        <span>沙盒：<code>${escapeHtml(execution.sandbox_path || "")}</code></span>
        <span>返回码：<code>${escapeHtml(execution.returncode ?? "—")}</code></span>
        <span>耗时：<code>${escapeHtml(execution.duration_ms || 0)}ms</code></span>
      </div>
      <h4>标准输出</h4>
      <pre class="run-output"><code>${escapeHtml(stdout || "（无输出）")}</code></pre>
      <h4>错误输出</h4>
      <pre class="run-output"><code>${escapeHtml(stderr || "（无错误输出）")}</code></pre>
      <p class="run-hint">运行结果已写入动作记录。若脚本只是生成练习产物但未自动保存完成记录，请在同一任务旁点击“记录并完成”补充备注。</p>
    </div>
  `;
}

function closeMarkdownViewer() {
  const modal = document.getElementById("readerModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function resolveReaderLink(href, baseFilePath) {
  const raw = String(href || "").trim();
  if (!raw || /^(?:[a-z][a-z0-9+.-]*:|#)/i.test(raw)) return "";
  const clean = raw.split("#")[0].split("?")[0];
  const baseDir = String(baseFilePath || "").split("/").slice(0, -1).join("/");
  const joined = clean.startsWith("/") ? clean.slice(1) : `${baseDir}/${clean}`;
  const parts = [];
  for (const part of joined.split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") {
      parts.pop();
      continue;
    }
    parts.push(part);
  }
  const normalized = parts.join("/");
  return READABLE_FILE_RE.test(normalized) ? normalized : "";
}

function inlineMarkdown(text, baseFilePath = "") {
  return escapeHtml(text)
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (match, label, href) => {
      if (/^https?:\/\//i.test(href)) {
        return `<a href="${href}" target="_blank" rel="noreferrer noopener">${label}</a>`;
      }
      const file = resolveReaderLink(href, baseFilePath);
      if (!file) return match;
      return `<a href="${file}" class="inline-doc-link" data-file="${file}" data-title="${label}">${label}</a>`;
    })
    .replace(/&lt;(https?:\/\/[^&]+)&gt;/g, '<a href="$1" target="_blank" rel="noreferrer noopener">$1</a>')
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function renderMarkdown(src, baseFilePath = "") {
  const lines = String(src).replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let paragraph = [];
  let list = [];
  let orderedList = [];
  let table = [];
  let code = [];
  let inCode = false;
  let codeLang = "";

  const flushParagraph = () => {
    if (!paragraph.length) return;
    out.push(`<p>${inlineMarkdown(paragraph.join(" "), baseFilePath)}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (!list.length) return;
    out.push(`<ul>${list.map((item) => `<li>${inlineMarkdown(item, baseFilePath)}</li>`).join("")}</ul>`);
    list = [];
  };
  const flushOrderedList = () => {
    if (!orderedList.length) return;
    out.push(`<ol>${orderedList.map((item) => `<li>${inlineMarkdown(item, baseFilePath)}</li>`).join("")}</ol>`);
    orderedList = [];
  };
  const flushTable = () => {
    if (!table.length) return;
    const rows = table
      .filter((line) => !/^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(line))
      .map((line) => line.replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim()));
    if (rows.length) {
      const head = rows[0];
      const body = rows.slice(1);
      out.push(`<div class="table-scroll"><table><thead><tr>${head.map((cell) => `<th>${inlineMarkdown(cell, baseFilePath)}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell, baseFilePath)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
    }
    table = [];
  };
  const flushBlocks = () => {
    flushParagraph();
    flushList();
    flushOrderedList();
    flushTable();
  };

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    const fence = line.match(/^```(\w+)?/);
    if (fence) {
      if (inCode) {
        out.push(`<pre><code class="language-${escapeHtml(codeLang)}">${escapeHtml(code.join("\n"))}</code></pre>`);
        code = [];
        codeLang = "";
        inCode = false;
      } else {
        flushBlocks();
        inCode = true;
        codeLang = fence[1] || "";
      }
      continue;
    }
    if (inCode) {
      code.push(rawLine);
      continue;
    }
    if (!line.trim()) {
      flushBlocks();
      continue;
    }
    if (/^\|.+\|$/.test(line)) {
      flushParagraph();
      flushList();
      table.push(line);
      continue;
    }
    flushTable();
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      flushOrderedList();
      flushList();
      const level = heading[1].length;
      out.push(`<h${level}>${inlineMarkdown(heading[2], baseFilePath)}</h${level}>`);
      continue;
    }
    if (/^---+$/.test(line.trim())) {
      flushBlocks();
      out.push("<hr>");
      continue;
    }
    if (line.startsWith("> ")) {
      flushBlocks();
      out.push(`<blockquote>${inlineMarkdown(line.slice(2), baseFilePath)}</blockquote>`);
      continue;
    }
    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      flushParagraph();
      flushOrderedList();
      list.push(bullet[1]);
      continue;
    }
    const ordered = line.match(/^\d+\.\s+(.+)$/);
    if (ordered) {
      flushParagraph();
      flushList();
      orderedList.push(ordered[1]);
      continue;
    }
    flushList();
    flushOrderedList();
    paragraph.push(line.trim());
  }
  if (inCode) {
    out.push(`<pre><code class="language-${escapeHtml(codeLang)}">${escapeHtml(code.join("\n"))}</code></pre>`);
  }
  flushBlocks();
  return `<div class="md-body">${out.join("\n")}</div>`;
}

function renderCodeDocument(src, filePath) {
  const ext = filePath.split(".").pop() || "";
  return `<div class="md-body code-doc"><p class="code-doc-note">这是练习脚本内容，可先在这里阅读步骤，再按任务要求练习。</p><pre><code class="language-${escapeHtml(ext)}">${escapeHtml(src)}</code></pre></div>`;
}

function bindReaderDocumentLinks(container) {
  if (!container) return;
  container.querySelectorAll(".inline-doc-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const file = link.getAttribute("data-file") || "";
      if (!file) return;
      openInlineReader(file, link.getAttribute("data-title") || file, "", { silent: true });
      closeMarkdownViewer();
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const closeBtn = document.getElementById("readerClose");
  const modal = document.getElementById("readerModal");
  const terminalInput = document.getElementById("terminalInput");
  const terminalRun = document.getElementById("terminalRun");
  const terminalClear = document.getElementById("terminalClear");
  const terminalReset = document.getElementById("terminalReset");
  const inlinePopout = document.getElementById("inlineReaderPopout");
  const settingsLink = document.querySelector('a[href="#secondaryTools"]');
  const secondaryTools = document.getElementById("secondaryTools");
  if (closeBtn) closeBtn.addEventListener("click", closeMarkdownViewer);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeMarkdownViewer();
    });
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && modal.classList.contains("open")) {
      closeMarkdownViewer();
    }
  });
  if (terminalInput) {
    terminalInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        runTerminalCommand(terminalInput.value);
      }
    });
  }
  if (terminalRun && terminalInput) terminalRun.addEventListener("click", () => runTerminalCommand(terminalInput.value));
  if (terminalClear) terminalClear.addEventListener("click", () => runTerminalCommand("clear"));
  if (terminalReset) terminalReset.addEventListener("click", resetTerminal);
  if (inlinePopout) {
    inlinePopout.addEventListener("click", () => {
      const file = inlinePopout.dataset.file || inlineReaderFile;
      const title = inlinePopout.dataset.title || document.getElementById("inlineReaderTitle")?.textContent || "阅读";
      if (file) openMarkdownViewer(file, title);
    });
  }
  if (settingsLink && secondaryTools) {
    settingsLink.addEventListener("click", (e) => {
      e.preventDefault();
      secondaryTools.open = true;
      secondaryTools.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
});
