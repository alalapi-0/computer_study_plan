// progress_ui.js — Web 写操作、阅读器、任务反馈与动作记录

let feedbackMap = {};
let eventMap = {};
let apiReady = false;

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
    banner.innerHTML = "<strong>✓ 网页打卡已启用</strong> — 可直接在任务旁点击完成 / 撤销，无需切换终端。";
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
    const res = await fetch("/" + filePath.replace(/^\//, ""));
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
  return actionType || "动作";
}

function closeMarkdownViewer() {
  const modal = document.getElementById("readerModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/&lt;(https?:\/\/[^&]+)&gt;/g, '<a href="$1" target="_blank" rel="noreferrer">$1</a>')
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
  if (closeBtn) closeBtn.addEventListener("click", closeMarkdownViewer);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeMarkdownViewer();
    });
  }
});
