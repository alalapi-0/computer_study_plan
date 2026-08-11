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
let activeView = "home";
let currentKnowledgeFile = "rounds/round_00/final/command_cheatsheet.md";
let currentKnowledgeTitle = "Terminal 命令小抄";
let lastModalFocus = null;
let lastModalFocusTaskId = "";
let viewTransitionTimer = 0;
let inlineReaderRequestId = 0;
let modalReaderRequestId = 0;
let knowledgeRequestId = 0;
let initialLegacyAnchorId = "";
let forceTerminalVisible = false;

const VIEW_META = {
  home: { title: "今日学习", eyebrow: "LINUX FOUNDATIONS" },
  learn: { title: "学习工作区", eyebrow: "FOCUS WORKSPACE" },
  route: { title: "学习路线", eyebrow: "COURSE ROUTE" },
  review: { title: "复习与反馈", eyebrow: "REVIEW SIGNALS" },
  knowledge: { title: "知识手册", eyebrow: "FIELD MANUAL" },
  growth: { title: "成长与进度", eyebrow: "EVIDENCE OF GROWTH" },
  completion: { title: "阶段结算", eyebrow: "STAGE CHECKPOINT" },
};

function setElementText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function setProgressElement(id, pct, label = "") {
  const element = document.getElementById(id);
  if (!element) return;
  const value = Math.max(0, Math.min(100, Number(pct) || 0));
  element.style.width = `${value}%`;
  const container = element.parentElement;
  if (container) {
    container.setAttribute("role", "progressbar");
    container.setAttribute("aria-valuemin", "0");
    container.setAttribute("aria-valuemax", "100");
    container.setAttribute("aria-valuenow", String(value));
    if (label) container.setAttribute("aria-label", label);
  }
}

function normalizedViewName(value) {
  const key = String(value || "").replace(/^#/, "");
  const legacy = {
    today: "home",
    learnWorkspace: "learn",
    continueCard: "learn",
    inlineReaderPanel: "learn",
    terminal: "learn",
    rounds: "route",
    progress: "route",
    lanes: "route",
    secondaryTools: "growth",
    stages: "growth",
    config: "growth",
    saves: "growth",
  };
  const normalized = legacy[key] || key;
  return VIEW_META[normalized] ? normalized : "";
}

function focusLegacyAnchor(anchorId, behavior = "auto") {
  const anchor = document.getElementById(anchorId);
  const disclosure = anchor?.closest("details");
  if (disclosure) disclosure.open = true;
  anchor?.scrollIntoView({ behavior, block: "start" });
  if (anchor) {
    anchor.setAttribute("tabindex", "-1");
    anchor.focus({ preventScroll: true });
  }
}

function focusInitialLegacyAnchor() {
  if (!initialLegacyAnchorId) return;
  const anchorId = initialLegacyAnchorId;
  initialLegacyAnchorId = "";
  focusLegacyAnchor(anchorId);
}

function updateViewChrome(viewName) {
  const meta = VIEW_META[viewName] || VIEW_META.home;
  setElementText("pageTitle", meta.title);
  setElementText("pageEyebrow", meta.eyebrow);
  document.title = `${meta.title} · Linux 基础与工程实践`;
  document.querySelectorAll("[data-view-target]").forEach((item) => {
    const selected = item.dataset.viewTarget === viewName;
    item.classList.toggle("active", selected);
    if (item.matches("a[data-view-target]")) {
      if (selected) item.setAttribute("aria-current", "page");
      else item.removeAttribute("aria-current");
    } else {
      item.removeAttribute("aria-current");
    }
  });
}

function showView(requestedView, options = {}) {
  const viewName = normalizedViewName(requestedView) || "home";
  const target = document.querySelector(`[data-view="${viewName}"]`);
  if (!target) return;
  const current = document.querySelector(".app-view[data-view]:not([hidden])");
  const reducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
  const commit = () => {
    clearTimeout(viewTransitionTimer);
    document.querySelectorAll(".app-view[data-view]").forEach((view) => {
      const selected = view === target;
      view.hidden = !selected;
      view.setAttribute("aria-hidden", selected ? "false" : "true");
      view.classList.remove("is-leaving");
      view.classList.toggle("is-entering", selected);
    });
    activeView = viewName;
    updateViewChrome(viewName);
    if (options.scroll !== false) window.scrollTo({ top: 0, behavior: "auto" });
    if (options.focus) {
      target.setAttribute("tabindex", "-1");
      target.focus({ preventScroll: true });
    }
  };
  if (current && current !== target && !reducedMotion && options.animate !== false) {
    clearTimeout(viewTransitionTimer);
    current.classList.add("is-leaving");
    viewTransitionTimer = window.setTimeout(commit, 135);
  } else {
    commit();
  }
  if (options.updateHash !== false && window.location.hash !== `#${viewName}`) {
    history.pushState({ view: viewName }, "", `#${viewName}`);
  }
  if (viewName === "knowledge" && !document.getElementById("knowledgeReaderBody")?.dataset.loaded) {
    void openKnowledgeDoc(currentKnowledgeFile, currentKnowledgeTitle);
  }
}

function setupViewNavigation() {
  document.querySelectorAll("[data-view-target]").forEach((item) => {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      initialLegacyAnchorId = "";
      forceTerminalVisible = false;
      showView(item.dataset.viewTarget, { updateHash: true, focus: true });
    });
  });
  const handleHistory = () => {
    initialLegacyAnchorId = "";
    const rawHash = String(window.location.hash || "").replace(/^#/, "");
    const fromHash = normalizedViewName(window.location.hash);
    if (!fromHash) return;
    forceTerminalVisible = rawHash === "terminal";
    const isViewHash = !!VIEW_META[rawHash] || ["today", "learnWorkspace", "rounds", "secondaryTools"].includes(rawHash);
    showView(fromHash, { updateHash: false, scroll: isViewHash, focus: isViewHash });
    if (rawHash === "terminal") renderTerminal();
    if (!isViewHash) {
      window.setTimeout(() => focusLegacyAnchor(rawHash, "smooth"), 170);
    }
  };
  window.addEventListener("popstate", handleHistory);
  window.addEventListener("hashchange", handleHistory);
  const query = new URLSearchParams(window.location.search || "");
  const deepLinkedRound = query.has("round") || query.has("activeRound") || [...query.keys()].some((key) => /^round_?\d{1,2}$/i.test(key));
  const initialView = normalizedViewName(window.location.hash) || (deepLinkedRound ? "route" : "home");
  showView(initialView, { updateHash: false, scroll: false, animate: false });
  const initialHash = String(window.location.hash || "").replace(/^#/, "");
  forceTerminalVisible = initialHash === "terminal";
  if (initialHash && !VIEW_META[initialHash] && !["today", "learnWorkspace", "rounds", "secondaryTools"].includes(initialHash)) {
    initialLegacyAnchorId = initialHash;
  }
}

async function detectApi() {
  if (window.location.protocol === "file:") {
    apiReady = false;
  } else {
    try {
      const res = await fetch("/api/health?_=" + Date.now());
      apiReady = res.ok;
    } catch (_) {
      apiReady = false;
    }
  }
  document.getElementById("apiStatusDot")?.classList.toggle("online", apiReady);
  document.querySelector(".app-shell")?.setAttribute("data-app-ready", "true");
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
  try {
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
    if (!undo && workspaceTaskId === taskId) {
      workspaceTaskId = "";
      inlineReaderTaskId = "";
      activeTerminalTaskId = "";
    }
    showToast(undo ? "已撤销完成" : "已保存记录并完成", "ok");
    render();
    return data;
  } catch (error) {
    showToast(error.message || "网络连接中断，请重试", "error");
    return null;
  }
}

function showToast(msg, kind) {
  let el = document.getElementById("toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "toast";
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    document.body.appendChild(el);
  }
  el.className = `toast ${kind || ""} is-visible`;
  el.textContent = msg;
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.classList.remove("is-visible"); }, 2600);
  if (kind === "ok" || kind === "error" || kind === "warn") {
    showFeedbackPulse(kind);
  }
}

function showFeedbackPulse(kind) {
  if (window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches) return;
  const pulse = document.createElement("span");
  pulse.className = `feedback-flash ${kind}`;
  pulse.setAttribute("aria-hidden", "true");
  document.body.appendChild(pulse);
  pulse.addEventListener("animationend", () => pulse.remove(), { once: true });
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
  if (task.type === "exercise") return true;
  if (["test", "output"].includes(task.type)) {
    return /round_(?:00|01|02|06)/.test(meta?.round?.id || "");
  }
  return /\.(?:sh|py)$/i.test(task.file || "");
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
  // Contextual task jumps need the workspace to exist before we calculate the
  // scroll position, so skip the decorative page-exit delay here.
  showView("learn", { updateHash: true, scroll: false, animate: false });
  requestAnimationFrame(() => target?.scrollIntoView({ behavior: "smooth", block: "start" }));
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
  const idleForCurrentTask = !forceTerminalVisible && !activeTerminalTaskId && current && !taskUsesTerminal(current.task);
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
  forceTerminalVisible = false;
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

function allCourseTasks() {
  const rows = [];
  for (const round of ROUNDS || []) {
    for (const week of round.weeks || []) {
      for (const task of week.tasks || []) rows.push({ round, week, task });
    }
  }
  return rows;
}

function taskVerb(task) {
  return {
    reading: "阅读",
    exercise: "练习",
    test: "验收",
    output: "产出",
  }[task?.type] || "学习";
}

function reviewCandidates() {
  return allCourseTasks().map((entry) => {
    const events = eventsFor(entry.task.id);
    const feedback = feedbackFor(entry.task.id);
    const lastEvent = events[events.length - 1] || null;
    return { ...entry, events, feedback, lastEvent };
  }).filter((entry) => entry.events.length > 0).sort((a, b) => {
    return String(b.lastEvent?.timestamp || "").localeCompare(String(a.lastEvent?.timestamp || ""));
  });
}

function renderHome() {
  if (typeof findNextTask !== "function") return;
  const allIds = Object.keys(progressData || {});
  const doneCount = allIds.filter((id) => isTaskDone(id)).length;
  const routePct = allIds.length ? Math.round(doneCount / allIds.length * 100) : 0;
  const next = findNextTask();
  const reviews = reviewCandidates();

  setElementText("railProgressPct", `${routePct}%`);
  setElementText("railProgressMeta", `${doneCount} / ${allIds.length || 0} 个任务`);
  setProgressElement("railProgressBar", routePct, "课程总进度");
  setElementText("homeRoutePct", `${routePct}%`);
  setProgressElement("homeRouteBar", routePct, "课程路线进度");
  const homeAction = document.querySelector(".home-primary-action");
  const homeActionLabel = homeAction?.querySelector("span");

  if (!next) {
    const courseComplete = allIds.length > 0 && doneCount === allIds.length;
    setElementText("homeTaskKicker", courseComplete ? "COURSE / COMPLETE" : "COURSE / UNAVAILABLE");
    setElementText("homeTaskVerb", courseComplete ? "完成" : "等待");
    setElementText("homeTaskTitle", courseComplete ? "所有已注册任务均已完成" : "课程任务尚未载入");
    setElementText("homeTaskMeta", courseComplete ? "进入成长页查看阶段结算" : "请先同步课程数据");
    setElementText("homeModuleValue", courseComplete ? "完成" : "—");
    setProgressElement("homeModuleBar", courseComplete ? 100 : 0, "当前模块进度");
    if (homeAction) homeAction.dataset.viewTarget = courseComplete ? "growth" : "route";
    if (homeActionLabel) homeActionLabel.textContent = courseComplete ? "查看成长与结算" : "查看课程状态";
  } else {
    const roundTasks = (next.round.weeks || []).flatMap((week) => week.tasks || []);
    const roundDone = roundTasks.filter((task) => isTaskDone(task.id)).length;
    const roundPct = roundTasks.length ? Math.round(roundDone / roundTasks.length * 100) : 0;
    const taskIndex = Math.max(0, roundTasks.findIndex((task) => task.id === next.task.id));
    setElementText("homeTaskKicker", `CURRENT / ${String(taskIndex + 1).padStart(2, "0")}`);
    setElementText("homeTaskVerb", taskVerb(next.task));
    setElementText("homeTaskTitle", next.task.title);
    setElementText("homeTaskMeta", `${next.round.title} · ${next.week.title}`);
    setElementText("homeModuleValue", `${roundDone} / ${roundTasks.length}`);
    setProgressElement("homeModuleBar", roundPct, "当前模块进度");
    if (homeAction) homeAction.dataset.viewTarget = "learn";
    if (homeActionLabel) homeActionLabel.textContent = "进入当前任务";
  }

  if (reviews.length) {
    setElementText("homeReviewValue", reviews[0].task.title);
    setElementText("homeReviewMeta", `${reviews[0].events.length} 条动作记录 · 可复盘`);
  } else {
    setElementText("homeReviewValue", "暂无");
    setElementText("homeReviewMeta", "完成任务后可回看动作记录");
  }
}

function renderReview() {
  const queue = document.getElementById("reviewQueue");
  const feedbackEl = document.getElementById("feedbackOverview");
  const timeline = document.getElementById("actionTimeline");
  if (!queue || !feedbackEl || !timeline) return;

  const candidates = reviewCandidates();
  const timelineEvents = Object.entries(eventMap || {}).flatMap(([taskId, events]) => (
    (events || []).map((event) => ({ ...event, taskId }))
  )).sort((a, b) => String(b.timestamp || "").localeCompare(String(a.timestamp || "")));
  const doneCount = Object.keys(progressData || {}).filter((id) => isTaskDone(id)).length;
  setElementText("reviewDueCount", String(candidates.length));
  setElementText("reviewEventCount", String(timelineEvents.length));
  setElementText("reviewDoneCount", String(doneCount));

  if (!candidates.length) {
    queue.innerHTML = '<div class="empty-state">还没有可复盘的动作记录。先完成一个真实任务，系统会把反馈与记录带回这里。</div>';
  } else {
    queue.innerHTML = candidates.slice(0, 6).map((entry) => `
      <div class="review-item">
        <div><strong>${escapeHtml(entry.task.title)}</strong><p>${escapeHtml(entry.round.title)} · ${entry.events.length} 条记录</p></div>
        <button class="task-btn record task-record-open" type="button" data-task="${escapeHtml(entry.task.id)}">复盘</button>
      </div>
    `).join("");
    bindTaskActions(queue);
  }

  const feedbackRows = candidates.filter((entry) => entry.feedback).slice(0, 5);
  feedbackEl.innerHTML = feedbackRows.length ? feedbackRows.map((entry) => `
    <div class="feedback-item">
      <span class="feedback-kind">${escapeHtml(entry.feedback.feedback_type || "feedback")}</span>
      <strong>${escapeHtml(entry.task.title)}</strong>
      <p>${escapeHtml(entry.feedback.next_suggestion || entry.feedback.message || "暂无下一步建议")}</p>
    </div>
  `).join("") : '<div class="empty-state">尚无动作级反馈。这里不会用虚构数据填满空白。</div>';

  timeline.innerHTML = timelineEvents.length ? timelineEvents.slice(0, 10).map((event) => {
    const meta = taskMeta(event.taskId);
    return `
      <div class="timeline-item">
        <time>${escapeHtml(event.timestamp || "时间待同步")}</time>
        <strong>${escapeHtml(meta?.task?.title || event.taskId)}</strong>
        <p>${escapeHtml(actionLabel(event.action_type))}${event.note ? ` · ${escapeHtml(event.note)}` : ""}</p>
      </div>
    `;
  }).join("") : '<div class="empty-state">动作时间线为空。运行练习或记录完成后会在这里出现。</div>';
}

function moduleDisplayCode(roundId) {
  return {
    round_00: "00",
    round_01: "01",
    round_02: "02",
    round_06: "03",
    plan_vps: "04",
    plan_linux: "导览",
  }[roundId] || "—";
}

function roundHasOpenTasks(round) {
  return !!round && (round.weeks || []).some((week) => (week.tasks || []).some((task) => !isTaskDone(task.id)));
}

function nextOpenRoundAfter(roundIds) {
  const rounds = ROUNDS || [];
  const currentScope = new Set(roundIds || []);
  return rounds.find((round) => !currentScope.has(round.id) && roundHasOpenTasks(round)) || null;
}

function renderGrowth() {
  const tasks = Object.keys(progressData || {});
  const doneCount = tasks.filter((id) => isTaskDone(id)).length;
  const evidenceCount = Object.values(eventMap || {}).reduce((sum, events) => sum + (events?.length || 0), 0);
  const next = typeof findNextTask === "function" ? findNextTask() : null;
  setElementText("growthDoneValue", String(doneCount));
  setElementText("growthDoneMeta", `共 ${tasks.length} 项`);
  setElementText("growthEvidenceValue", String(evidenceCount));
  setElementText("growthModuleValue", next ? moduleDisplayCode(next.round.id) : "完成");
  setElementText("growthModuleMeta", next?.round?.title || "全部完成");
}

function renderCompletion() {
  const shell = document.getElementById("completionState");
  if (!shell) return;
  const round = (ROUNDS || []).find((item) => item.id === activeRound) || (typeof findNextTask === "function" ? findNextTask()?.round : null) || (ROUNDS || [])[0];
  if (!round) {
    shell.classList.remove("is-complete");
    shell.innerHTML = '<span class="completion-halo" aria-hidden="true"></span><div class="completion-copy"><span class="section-kicker">STAGE CHECKPOINT</span><h2 id="completionHeading">暂无阶段</h2><p>课程数据尚未载入。</p></div>';
    return;
  }
  const stage = typeof STAGES !== "undefined"
    ? STAGES.find((item) => item.round_ids?.includes(round.id))
    : null;
  const scopeRoundIds = stage?.round_ids?.length ? stage.round_ids : [round.id];
  const scopeRounds = (ROUNDS || []).filter((item) => scopeRoundIds.includes(item.id));
  const tasks = scopeRounds.flatMap((item) => (item.weeks || []).flatMap((week) => week.tasks || []));
  const doneCount = tasks.filter((task) => isTaskDone(task.id)).length;
  const pct = tasks.length ? Math.round(doneCount / tasks.length * 100) : 0;
  const complete = tasks.length > 0 && doneCount === tasks.length;
  const nextRound = complete ? nextOpenRoundAfter(scopeRoundIds) : null;
  const scopeTitle = stage?.name || round.title;
  const scopeKind = stage ? "阶段" : "资料组";
  const actionTarget = complete ? "route" : "learn";
  const actionLabel = complete ? (nextRound ? "继续未完成模块" : "返回学习路线") : "继续当前任务";
  shell.classList.toggle("is-complete", complete);
  shell.innerHTML = `
    <span class="completion-halo" aria-hidden="true"></span>
    <div class="completion-copy">
      <span class="section-kicker">${complete ? "STAGE COMPLETE" : "STAGE CHECKPOINT"}</span>
      <h2 id="completionHeading">${complete ? `${scopeKind}完成` : "继续推进"}</h2>
      <p>${escapeHtml(scopeTitle)} · ${complete ? `全部 ${tasks.length} 个任务已标记完成。` : `还有 ${Math.max(0, tasks.length - doneCount)} 个任务等待完成。`}</p>
      <div class="completion-progress"><strong>${doneCount} / ${tasks.length} · ${pct}%</strong><div class="route-track" role="progressbar" aria-label="${escapeHtml(scopeTitle)}进度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><span style="width:${pct}%"></span></div></div>
      <div class="completion-actions"><button class="physical-button" type="button" data-view-target="${actionTarget}"${nextRound ? ` data-round-target="${escapeHtml(nextRound.id)}"` : ""}><span>${actionLabel}</span><span aria-hidden="true">→</span></button></div>
    </div>
  `;
  shell.querySelectorAll("[data-view-target]").forEach((button) => {
    button.addEventListener("click", () => {
      const targetRound = (ROUNDS || []).find((item) => item.id === button.dataset.roundTarget);
      if (targetRound) {
        activeLane = targetRound.lane || activeLane;
        activeRound = targetRound.id;
        workspaceTaskId = "";
        routeFocusedRound = true;
        render();
      }
      showView(button.dataset.viewTarget, { updateHash: true, focus: true });
    });
  });
}

async function openKnowledgeDoc(filePath, title) {
  const body = document.getElementById("knowledgeReaderBody");
  const heading = document.getElementById("knowledgeReaderTitle");
  if (!body || !heading || !filePath) return;
  const requestId = ++knowledgeRequestId;
  currentKnowledgeFile = filePath;
  currentKnowledgeTitle = title || filePath;
  heading.textContent = currentKnowledgeTitle;
  body.innerHTML = '<p class="reader-loading">正在加载手册…</p>';
  document.querySelectorAll(".knowledge-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.knowledgeFile === filePath);
  });
  try {
    const resourcePath = "/" + filePath.replace(/^\//, "");
    const res = await fetch(`${resourcePath}?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    if (requestId !== knowledgeRequestId) return;
    body.innerHTML = /\.(sh|py|js|json)$/i.test(filePath)
      ? renderCodeDocument(text, filePath)
      : renderMarkdown(text, filePath);
    body.dataset.loaded = "true";
    body.querySelectorAll(".inline-doc-link").forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const linkedFile = link.dataset.file || "";
        if (linkedFile) void openKnowledgeDoc(linkedFile, link.dataset.title || linkedFile);
      });
    });
  } catch (error) {
    if (requestId !== knowledgeRequestId) return;
    body.innerHTML = `<p class="reader-error">无法加载 ${escapeHtml(filePath)}：${escapeHtml(error.message)}</p>`;
  }
}

function setupKnowledge() {
  document.querySelectorAll(".knowledge-item").forEach((item) => {
    item.addEventListener("click", () => void openKnowledgeDoc(item.dataset.knowledgeFile || "", item.dataset.knowledgeTitle || item.textContent.trim()));
  });
  document.getElementById("knowledgeReaderPopout")?.addEventListener("click", () => {
    openMarkdownViewer(currentKnowledgeFile, currentKnowledgeTitle);
  });
}

function setupSpatialInteraction() {
  const stage = document.getElementById("spatialStage");
  if (!stage) return;
  const blocks = [...stage.querySelectorAll(".spatial-block")];
  const depths = [-13, -8, -3, 5, 9, 14];
  const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
  const setParallax = (x, y) => {
    if (reduced) return;
    stage.style.setProperty("--warm-x", `${x * -10}px`);
    stage.style.setProperty("--warm-y", `${y * -6}px`);
    stage.style.setProperty("--cool-x", `${x * 9}px`);
    stage.style.setProperty("--cool-y", `${y * 6}px`);
    stage.style.setProperty("--card-x", `${x * 7}px`);
    stage.style.setProperty("--card-y", `${y * 5}px`);
    stage.style.setProperty("--card-tilt-x", `${y * -2}deg`);
    stage.style.setProperty("--card-tilt-y", `${x * 3}deg`);
    blocks.forEach((block, index) => {
      block.style.setProperty("--parallax-x", `${x * depths[index]}px`);
      block.style.setProperty("--parallax-y", `${y * depths[index] * 0.52}px`);
    });
  };
  stage.addEventListener("pointermove", (event) => {
    if (event.pointerType === "touch") return;
    const rect = stage.getBoundingClientRect();
    setParallax((event.clientX - rect.left) / rect.width - 0.5, (event.clientY - rect.top) / rect.height - 0.5);
  });
  stage.addEventListener("pointerleave", () => setParallax(0, 0));

  blocks.forEach((block) => {
    let drag = null;
    block.addEventListener("pointerdown", (event) => {
      drag = { x: event.clientX, y: event.clientY };
      block.classList.add("is-dragging");
      block.setPointerCapture?.(event.pointerId);
    });
    block.addEventListener("pointermove", (event) => {
      if (!drag) return;
      const dx = Math.max(-34, Math.min(34, event.clientX - drag.x));
      const dy = Math.max(-26, Math.min(26, event.clientY - drag.y));
      block.style.setProperty("--drag-x", `${dx}px`);
      block.style.setProperty("--drag-y", `${dy}px`);
    });
    const release = () => {
      if (!drag) return;
      drag = null;
      block.classList.remove("is-dragging");
      block.style.setProperty("--drag-x", "0px");
      block.style.setProperty("--drag-y", "0px");
    };
    block.addEventListener("pointerup", release);
    block.addEventListener("pointercancel", release);
    block.addEventListener("lostpointercapture", release);
  });
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
  try {
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
    if (isTaskDone(taskId)) {
      if (workspaceTaskId === taskId) workspaceTaskId = "";
      if (activeTerminalTaskId === taskId) activeTerminalTaskId = "";
    }
    render();
    openExecutionResult(title, data.execution || {});
    const result = data.execution?.result || "";
    showToast(result === "ok" ? "练习脚本运行完成" : "练习脚本已结束，请查看输出", result === "ok" ? "ok" : "warn");
    return data;
  } catch (error) {
    showToast(error.message || "练习脚本请求失败", "error");
    return null;
  }
}

function bindTaskActions(container) {
  container.querySelectorAll(".task-btn[data-action]").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.getAttribute("data-task");
      const undo = btn.getAttribute("data-action") === "undo";
      btn.disabled = true;
      try { await postTaskAction(id, undo); } finally { btn.disabled = false; }
    });
  });
  container.querySelectorAll(".task-record-open").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      lastModalFocus = btn;
      lastModalFocusTaskId = btn.getAttribute("data-task") || "";
      openRecordViewer(btn.getAttribute("data-task"));
    });
  });
  container.querySelectorAll(".task-complete-open").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      lastModalFocus = btn;
      lastModalFocusTaskId = btn.getAttribute("data-task") || "";
      openRecordViewer(btn.getAttribute("data-task"), { requireNote: true });
    });
  });
  container.querySelectorAll(".task-run").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.getAttribute("data-task");
      btn.disabled = true;
      try { await postTaskRun(id); } finally { btn.disabled = false; }
    });
  });
  container.querySelectorAll(".task-terminal").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      btn.disabled = true;
      try { await openTaskTerminal(btn.getAttribute("data-task")); } finally { btn.disabled = false; }
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
  const requestId = ++inlineReaderRequestId;
  const body = document.getElementById("inlineReaderBody");
  const heading = document.getElementById("inlineReaderTitle");
  const metaEl = document.getElementById("inlineReaderMeta");
  const popout = document.getElementById("inlineReaderPopout");
  if (!body || !heading) {
    openMarkdownViewer(filePath, title);
    return;
  }
  if (taskId) {
    if (!options?.silent) forceTerminalVisible = false;
    workspaceTaskId = taskId;
    routeFocusedRound = false;
    const meta = taskMeta(taskId);
    if (meta) {
      activeLane = meta.round.lane || activeLane;
      activeRound = meta.round.id || activeRound;
    }
    if (activeTerminalTaskId && activeTerminalTaskId !== taskId) activeTerminalTaskId = "";
  }
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
  if (taskId) {
    renderContinue();
    renderTerminal();
  }
  if (!options?.silent) {
    scrollWorkspacePanel("inlineReaderPanel");
  }
  try {
    const resourcePath = "/" + filePath.replace(/^\//, "");
    const separator = resourcePath.includes("?") ? "&" : "?";
    const res = await fetch(`${resourcePath}${separator}_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    if (requestId !== inlineReaderRequestId) return;
    body.innerHTML = /\.(sh|py|js|json)$/i.test(filePath)
      ? renderCodeDocument(text, filePath)
      : renderMarkdown(text, filePath);
    bindReaderDocumentLinks(body);
  } catch (err) {
    if (requestId !== inlineReaderRequestId) return;
    body.innerHTML = `<p class='reader-error'>无法加载 ${escapeHtml(filePath)}：${escapeHtml(err.message)}</p>`;
  }
}

async function openMarkdownViewer(filePath, title) {
  if (!filePath) return;
  const requestId = ++modalReaderRequestId;
  const modal = document.getElementById("readerModal");
  const body = document.getElementById("readerBody");
  const heading = document.getElementById("readerTitle");
  if (!modal || !body) return;
  heading.textContent = title || filePath;
  body.innerHTML = "<p class='reader-loading'>加载中…</p>";
  revealReaderModal();
  try {
    const resourcePath = "/" + filePath.replace(/^\//, "");
    const separator = resourcePath.includes("?") ? "&" : "?";
    const res = await fetch(`${resourcePath}${separator}_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    if (requestId !== modalReaderRequestId) return;
    if (/\.(sh|py|js|json)$/i.test(filePath)) {
      body.innerHTML = renderCodeDocument(text, filePath);
    } else {
      body.innerHTML = renderMarkdown(text, filePath);
    }
    bindReaderDocumentLinks(body);
  } catch (err) {
    if (requestId !== modalReaderRequestId) return;
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
  modalReaderRequestId += 1;
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
  revealReaderModal();

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
    try {
      const result = await postTaskAction(taskId, undo, { note, evidence_path: evidencePath });
      if (result) closeMarkdownViewer();
    } finally {
      if (btn?.isConnected) btn.disabled = false;
    }
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
  const noteRequired = options.requireNote || !done;
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
      <label class="record-label" for="recordNote">本次记录${noteRequired ? "（必填）" : "（建议填写）"}</label>
      <textarea id="recordNote" class="record-input"${noteRequired ? ' required aria-required="true"' : ""} placeholder="${escapeHtml(placeholders.note)}"></textarea>
      <label class="record-label" for="recordEvidence">证据路径（可选）</label>
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
  modalReaderRequestId += 1;
  const modal = document.getElementById("readerModal");
  const body = document.getElementById("readerBody");
  const heading = document.getElementById("readerTitle");
  if (!modal || !body || !heading) return;
  heading.textContent = `运行结果 · ${title}`;
  body.innerHTML = renderExecutionResult(execution);
  revealReaderModal();
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

function revealReaderModal() {
  const modal = document.getElementById("readerModal");
  if (!modal) return;
  if (!lastModalFocus?.isConnected) {
    lastModalFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  }
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
  document.querySelector(".app-shell")?.setAttribute("inert", "");
  requestAnimationFrame(() => document.getElementById("readerClose")?.focus({ preventScroll: true }));
}

function closeMarkdownViewer() {
  const modal = document.getElementById("readerModal");
  if (!modal) return;
  modalReaderRequestId += 1;
  const visibleTaskTarget = lastModalFocusTaskId
    ? [...document.querySelectorAll(`[data-task="${CSS.escape(lastModalFocusTaskId)}"]`)].find((element) => element instanceof HTMLElement && element.offsetParent !== null)
    : null;
  const focusTarget = lastModalFocus?.isConnected
    ? lastModalFocus
    : visibleTaskTarget || document.querySelector(".app-view:not([hidden])");
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
  document.querySelector(".app-shell")?.removeAttribute("inert");
  if (focusTarget) {
    if (!focusTarget.hasAttribute("tabindex") && !focusTarget.matches("button, a, input, textarea, select, summary")) {
      focusTarget.setAttribute("tabindex", "-1");
    }
    focusTarget.focus({ preventScroll: true });
    // Keep keyboard dismissal deterministic after the browser finishes
    // dispatching Escape and applies its own default focus behavior.
    requestAnimationFrame(() => {
      if (focusTarget.isConnected && !modal.classList.contains("open")) {
        focusTarget.focus({ preventScroll: true });
      }
    });
  }
  lastModalFocus = null;
  lastModalFocusTaskId = "";
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
  setupViewNavigation();
  setupKnowledge();
  setupSpatialInteraction();
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
      return;
    }
    if (e.key === "Tab" && modal?.classList.contains("open")) {
      const focusable = [...modal.querySelectorAll('button:not([disabled]), a[href], input:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])')]
        .filter((element) => element instanceof HTMLElement && element.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
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
