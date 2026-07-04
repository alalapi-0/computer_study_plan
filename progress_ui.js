// progress_ui.js — Web 写操作、阅读器、任务反馈与动作记录

let feedbackMap = {};
let eventMap = {};
let apiReady = false;
let terminalHistory = [];
let terminalCwd = "";
let terminalCwdDisplay = "~";
let terminalStateInfo = null;
let activeTerminalTaskId = "";

const TERMINAL_QUICK_COMMANDS = [
  "pwd",
  "ls",
  "ls -la",
  "cat next_steps.txt",
  "git status",
  "git log --oneline --max-count=5",
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
    banner.innerHTML = "<strong>网页打卡已启用</strong> — 可直接在任务旁点击完成 / 撤销，无需切换终端。";
    banner.style.display = "block";
  } else if (window.location.protocol !== "file:") {
    banner.className = "banner warn";
    banner.innerHTML =
      '<strong>只读模式</strong> — 请用 <code>python3 scripts/progress_server.py</code> 启动以启用网页打卡。';
    banner.style.display = "block";
  } else {
    banner.className = "banner warn";
    banner.innerHTML =
      '<strong>本地文件模式</strong> — 建议运行 <code>python3 scripts/progress_server.py</code> 后访问看板。';
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
  showToast(undo ? "已撤销完成" : "已标记完成", "ok");
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

function terminalCwdForRound(round) {
  const match = String(round?.id || "").match(/round_(\d{2})/);
  if (!match) return "~";
  return `~/round${Number(match[1])}`;
}

function terminalTaskTarget(taskId) {
  const meta = taskMeta(taskId);
  if (!meta) return "~";
  return terminalCwdForRound(meta.round);
}

function taskUsesTerminal(task) {
  if (!task) return false;
  const meta = taskMeta(task.id);
  if (meta?.round?.lane !== "engineering") return false;
  return ["exercise", "test", "output"].includes(task.type);
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
    quickEl.innerHTML = TERMINAL_QUICK_COMMANDS.map((cmd) => (
      `<button type="button" class="terminal-chip" data-command="${escapeHtml(cmd)}">${escapeHtml(cmd)}</button>`
    )).join("");
    quickEl.querySelectorAll(".terminal-chip").forEach((btn) => {
      btn.addEventListener("click", () => runTerminalCommand(btn.getAttribute("data-command") || ""));
    });
  }
  if (!contextEl) return;
  const meta = terminalTaskContext();
  if (!meta) {
    contextEl.innerHTML = `
      <div class="terminal-context-title">未绑定任务</div>
      <div class="terminal-context-meta">从任务行点击“终端”，这里会切到对应 Round 的沙盒目录。</div>
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
      ${canRead ? `<button type="button" class="task-btn read task-open" data-file="${escapeHtml(meta.task.file)}" data-title="${escapeHtml(meta.task.title)}">打开资料</button>` : ""}
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
  prompt.textContent = terminalPrompt(terminalCwdDisplay || "~");
  renderTerminalContext();
  if (!terminalHistory.length) {
    output.innerHTML = `<div class="terminal-line muted">终端已映射到 <code>~/cli-lab</code> 沙盒。任务行的“终端”会把这里切到对应 Round 目录。</div>`;
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
    terminalHistory = [{ kind: "error", prompt: "~ $", command: "", error: "请用 python3 scripts/progress_server.py 启动后使用练习终端。", cwd_display: "~" }];
    renderTerminal();
    if (input) input.disabled = true;
    return;
  }
  if (input) input.disabled = false;
  try {
    const res = await fetch(`/api/terminal?cwd=${encodeURIComponent(terminalCwd || "")}&_=${Date.now()}`);
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
    document.getElementById("terminal")?.scrollIntoView({ behavior: "smooth", block: "start" });
    setTimeout(() => document.getElementById("terminalInput")?.focus(), 220);
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
  await runTerminalCommand("cd ~");
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
  return `<button type="button" class="task-btn done" data-task="${taskId}" data-action="done">完成</button>`;
}

function taskRecordButton(taskId) {
  if (!apiReady) return "";
  const count = eventsFor(taskId).length;
  const label = count ? `记录 ${count}` : "记录";
  return `<button type="button" class="task-btn record task-record-open" data-task="${taskId}">${label}</button>`;
}

function isRunnableTask(task) {
  return !!(task && /\.(sh|py)$/i.test(task.file || "") && task.type === "exercise");
}

function taskRunButton(task) {
  if (!apiReady || !isRunnableTask(task)) return "";
  return `<button type="button" class="task-btn run task-run" data-task="${task.id}">运行</button>`;
}

function taskTerminalButton(task) {
  if (!apiReady || !taskUsesTerminal(task)) return "";
  return `<button type="button" class="task-btn terminal task-terminal" data-task="${task.id}">终端</button>`;
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
    `将在本地沙盒执行白名单练习脚本：\n${file}\n\n工作目录：${sandbox}\n脚本可能写入沙盒、调用打卡脚本并追加动作记录。继续？`
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
      openMarkdownViewer(btn.getAttribute("data-file"), btn.getAttribute("data-title") || "阅读");
    });
  });
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
      body.innerHTML = renderMarkdown(text);
    }
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

function openRecordViewer(taskId) {
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
  body.innerHTML = renderRecordBody(taskId, done, fb, events);
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");

  const saveBtn = body.querySelector("#recordSaveDone");
  const undoBtn = body.querySelector("#recordUndoDone");
  const action = async (undo) => {
    const note = body.querySelector("#recordNote")?.value || "";
    const evidencePath = body.querySelector("#recordEvidence")?.value || "";
    const btn = undo ? undoBtn : saveBtn;
    if (btn) btn.disabled = true;
    await postTaskAction(taskId, undo, { note, evidence_path: evidencePath });
    closeMarkdownViewer();
  };
  if (saveBtn) saveBtn.addEventListener("click", () => action(false));
  if (undoBtn) undoBtn.addEventListener("click", () => action(true));
}

function renderRecordBody(taskId, done, fb, events) {
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
      <p class="record-suggestion">${escapeHtml(fb?.next_suggestion || "")}</p>
      <label class="record-label">本次备注（可选）</label>
      <textarea id="recordNote" class="record-input" placeholder="例如：读完第 1 小节，命令还需要复习。"></textarea>
      <label class="record-label">证据路径（可选）</label>
      <input id="recordEvidence" class="record-input" placeholder="例如：~/cli-lab/round0/week1" />
      <div class="record-actions">
        <button type="button" class="task-btn done" id="recordSaveDone">${done ? "保存备注并保持完成" : "保存并标记完成"}</button>
        ${done ? '<button type="button" class="task-btn undo" id="recordUndoDone">撤销完成</button>' : ""}
      </div>
      <h4>最近记录</h4>
      <ul class="record-list">${eventRows}</ul>
    </div>
  `;
}

function actionLabel(actionType) {
  if (actionType === "mark_done") return "标记完成";
  if (actionType === "undo_done") return "撤销完成";
  if (actionType === "run_exercise") return "运行练习";
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
      <p class="run-hint">运行结果已写入动作记录。若脚本只是生成练习产物但未自动打卡，请在同一任务旁点击“完成”或打开“记录”补充备注。</p>
    </div>
  `;
}

function closeMarkdownViewer() {
  const modal = document.getElementById("readerModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer noopener">$1</a>')
    .replace(/&lt;(https?:\/\/[^&]+)&gt;/g, '<a href="$1" target="_blank" rel="noreferrer noopener">$1</a>')
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function renderMarkdown(src) {
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
    out.push(`<p>${inlineMarkdown(paragraph.join(" "))}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (!list.length) return;
    out.push(`<ul>${list.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</ul>`);
    list = [];
  };
  const flushOrderedList = () => {
    if (!orderedList.length) return;
    out.push(`<ol>${orderedList.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</ol>`);
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
      out.push(`<div class="table-scroll"><table><thead><tr>${head.map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
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
      out.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }
    if (/^---+$/.test(line.trim())) {
      flushBlocks();
      out.push("<hr>");
      continue;
    }
    if (line.startsWith("> ")) {
      flushBlocks();
      out.push(`<blockquote>${inlineMarkdown(line.slice(2))}</blockquote>`);
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

document.addEventListener("DOMContentLoaded", () => {
  const closeBtn = document.getElementById("readerClose");
  const modal = document.getElementById("readerModal");
  const terminalInput = document.getElementById("terminalInput");
  const terminalRun = document.getElementById("terminalRun");
  const terminalClear = document.getElementById("terminalClear");
  const terminalReset = document.getElementById("terminalReset");
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
});
