"use strict";

(() => {
  const RR_MODE = location.origin === "https://rr-computer-study-plan.invalid:9419";
  const HINT_KEY = "csp_problem_hints_v1";
  const ATTEMPT_KEY = "csp_problem_current_attempt_v1";
  const POLL_MS = 700;
  const state = {
    token: "", capabilities: {}, scenarios: [], attempts: [], selected: null,
    current: null, cursor: 0, terminal: null, fitTimer: 0, pollTimer: 0, resizeAbortController: null, lastResizeKey: "",
    generation: 0, controller: null, pending: null, hintOn: localStorage.getItem(HINT_KEY) === "on",
    query: "", tag: "all", solutionOpen: false, preViewed: {}, revisions: new Map(),
    locateOnly: new URLSearchParams(location.search).get("locate") === "1",
    artifactPending: false, artifactOperation: null, artifactReceipt: null, artifactNotice: null, artifactSelection: null, artifactCheckKey: null,
    inputQueue: [], inputTimer: 0, inputDrain: null, inputUncertain: null,
  };
  const $ = (id) => document.getElementById(id);
  const els = {};
  const ids = ["exportWavButton","downloadWavButton","artifactState","artifactProvenance","hintToggle","catalogCount","scenarioSearch","tagFilters","catalogStatus","scenarioList","globalError","capabilityNotice","problemTitle","scenarioMeta","problemSummary","startButton","problemFacts","problemSymptom","problemGoal","problemConstraints","problemProvenance","problemPublication","guideCard","practiceGrid","labPanel","labHeading","attemptStatus","differentScenarioNotice","environmentFacts","terminal","terminalTarget","terminalMessage","ctrlCButton","reconnectButton","hintsClosed","hintsPanel","hintSteps","solutionButton","solutionPanel","solutionExplanation","solutionSteps","checkButton","stopButton","resetButton","operationState","checksEmpty","checksList","refreshHistory","historyStatus","attemptHistory","resetDialog","confirmReset"];
  ids.forEach((id) => { els[id] = $(id); });

  function asText(value, fallback = "待验证") {
    return typeof value === "string" && value.trim() ? value.trim() : fallback;
  }
  function displayValue(value, fallback = "待验证") {
    if (typeof value === "string" && value.trim()) return value.trim();
    if (typeof value === "number" && Number.isFinite(value)) return String(value);
    return fallback;
  }
  function array(value) { return Array.isArray(value) ? value : []; }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
  function make(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  }
  function operationId() {
    return crypto.randomUUID ? crypto.randomUUID() : `op-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }
  function attemptMap() {
    try { return JSON.parse(sessionStorage.getItem(ATTEMPT_KEY) || "{}") || {}; } catch (_) { return {}; }
  }
  function rememberAttempt(attempt) {
    if (!attempt?.scenario_id || !attempt?.id) return;
    const map = attemptMap(); map[attempt.scenario_id] = attempt.id;
    sessionStorage.setItem(ATTEMPT_KEY, JSON.stringify(map));
  }
  function urlFor(scenarioId, attemptId) {
    if (RR_MODE) return "/";
    const url = new URL(location.href); url.search = "";
    if (scenarioId) url.searchParams.set("scenario", scenarioId);
    if (state.locateOnly) url.searchParams.set("locate", "1");
    if (attemptId) url.searchParams.set("attempt", attemptId);
    return `${url.pathname}${url.search}`;
  }
  function setUrl(scenarioId, attemptId, mode = "replace") {
    const value = urlFor(scenarioId, attemptId);
    const current = `${location.pathname}${location.search}`;
    if (value === current) return;
    history[mode === "push" ? "pushState" : "replaceState"]({ scenarioId, attemptId }, "", value);
  }
  function showError(message) {
    els.globalError.textContent = message; els.globalError.hidden = !message;
  }
  function abortRequests() {
    cancelResize();
    state.generation += 1;
    if (state.controller) state.controller.abort();
    state.controller = new AbortController();
    clearTimeout(state.pollTimer);
  }
  async function request(path, options = {}) {
    if (RR_MODE) {
      if (options.method && options.method !== "GET") throw new Error("远程审核为只读模式，请在本机操作实验。");
      if (path !== "/api/lab/bootstrap") throw new Error("此数据不在本次远程审核范围内。");
      path = "/__rr/v1/workbench";
    }
    const headers = new Headers(options.headers || {});
    if (state.token && path !== "/api/lab/bootstrap") headers.set("X-Lab-Token", state.token);
    if (options.body) headers.set("Content-Type", "application/json");
    const response = await fetch(path, { ...options, headers });
    let data;
    try { data = await response.json(); } catch (_) { data = {}; }
    if (!response.ok) {
      const error = new Error(asText(data.error, `请求失败（HTTP ${response.status}）`));
      error.status = response.status; error.definitive = response.status >= 400 && response.status < 500;
      throw error;
    }
    return data;
  }
  function capabilitySummary() {
    const cap = state.capabilities || {};
    const available = cap.available === true;
    const versions = cap.versions && typeof cap.versions === "object" ? cap.versions : {};
    const pick = (...keys) => keys.map((key) => versions[key]).find((value) => value !== undefined);
    const os = displayValue(pick("operating_system", "host_userland", "userland", "os"), "Linux 用户态");
    const arch = displayValue(pick("architecture", "arch"), "架构待验证");
    const shell = displayValue(pick("bash", "shell"), "Bash");
    const python = displayValue(pick("python3", "python"), "Python 待验证");
    const translations = {
      "single-node host userland, not an Ubuntu image": "单节点宿主用户态，不是 Ubuntu 镜像",
      "single-node host userland, not a separate distribution image": "单节点宿主用户态，不是独立发行版镜像",
      "no network, systemd, kernel administration, VM, macOS, or Windows semantics": "无网络、systemd、内核管理、虚拟机、macOS 或 Windows 语义",
      "workspace is disposable and limited to one active lab": "工作区可丢弃，同时只运行一个练习环境",
    };
    clear(els.capabilityNotice); els.capabilityNotice.hidden = false;
    if (RR_MODE) {
      els.capabilityNotice.textContent = "远程只读审核：当前展示实际题库内容。终端、实验操作和个人尝试记录仅在本机开放。";
      const feedbackLink = make("a", "提交审核反馈", "rr-feedback-link"); feedbackLink.href = "#rrFeedbackMount"; els.capabilityNotice.append(feedbackLink);
      return;
    }
    els.capabilityNotice.appendChild(make("strong", available ? `隔离环境可用：${os} · ${arch} · ${shell} · ${python}` : "隔离环境当前不可用"));
    const details = make("details"); details.appendChild(make("summary", "查看环境边界与完整版本"));
    const limits = make("ul");
    const limitations = array(cap.limitations).length ? array(cap.limitations) : [asText(cap.limitations, "环境能力尚未完成验证")];
    limitations.forEach((item) => limits.appendChild(make("li", translations[item] || item)));
    details.appendChild(limits);
    const versionList = make("dl");
    Object.entries(versions).forEach(([key, value]) => { const row = make("div"); row.append(make("dt", `${key.replaceAll("_", " ")}：`), make("dd", String(value))); versionList.appendChild(row); });
    details.appendChild(versionList); els.capabilityNotice.appendChild(details);
  }
  function scenarioById(id) { return state.scenarios.find((item) => item.id === id) || null; }

  function renderFilters() {
    clear(els.tagFilters);
    const tags = [...new Set(state.scenarios.flatMap((scenario) => array(scenario.tags)))].sort();
    ["all", ...tags].forEach((tag) => {
      const button = make("button", tag === "all" ? "全部" : tag, "tag");
      button.type = "button"; button.dataset.tag = tag;
      button.setAttribute("aria-pressed", String(state.tag === tag));
      button.addEventListener("click", () => { state.tag = tag; renderFilters(); renderCatalog(); });
      els.tagFilters.appendChild(button);
    });
  }
  function renderCatalog() {
    clear(els.scenarioList);
    const query = state.query.trim().toLocaleLowerCase("zh-CN");
    const results = state.scenarios.filter((scenario) => {
      const tagMatch = state.tag === "all" || array(scenario.tags).includes(state.tag);
      const search = [scenario.title, scenario.summary, scenario.symptom, ...array(scenario.tags)].join(" ").toLocaleLowerCase("zh-CN");
      return tagMatch && (!query || search.includes(query));
    });
    els.catalogCount.textContent = `${results.length} / ${state.scenarios.length}`;
    els.catalogStatus.hidden = results.length > 0;
    els.catalogStatus.textContent = state.scenarios.length ? "没有符合筛选的题目。" : "题库为空。";
    results.forEach((scenario) => {
      const li = make("li", undefined, "scenario-item");
      const button = make("button"); button.type = "button";
      button.setAttribute("aria-current", String(state.selected?.id === scenario.id));
      button.append(make("strong", asText(scenario.title)), make("small", asText(scenario.summary, "暂无摘要")));
      const tags = make("span", undefined, "mini-tags");
      array(scenario.tags).forEach((tag) => tags.appendChild(make("span", tag)));
      button.appendChild(tags);
      button.addEventListener("click", () => selectScenario(scenario.id, { historyMode: "push", loadRemembered: false }));
      li.appendChild(button); els.scenarioList.appendChild(li);
    });
  }
  function addConstraint(value) { els.problemConstraints.appendChild(make("li", typeof value === "string" ? value : JSON.stringify(value))); }
  function renderProvenance(provenance) {
    clear(els.problemProvenance);
    if (!provenance || typeof provenance !== "object") { els.problemProvenance.textContent = asText(provenance); return; }
    Object.entries(provenance).forEach(([key, value]) => {
      const labels = { type: "类型", kind: "类型", status: "状态", source_links: "来源链接", adaptations: "教学改编" };
      const row = make("p"); row.appendChild(make("strong", `${labels[key] || key}：`));
      if (key === "source_links" && Array.isArray(value)) {
        value.forEach((entry, index) => {
          let url;
          try { url = new URL(String(entry)); } catch (_) { url = null; }
          if (url?.protocol === "https:") {
            if (index) row.appendChild(document.createTextNode("；"));
            const link = make("a", url.hostname); link.href = url.href; link.rel = "noopener noreferrer"; link.target = "_blank"; row.appendChild(link);
          }
        });
      } else row.appendChild(document.createTextNode(Array.isArray(value) ? value.join("；") : String(value)));
      els.problemProvenance.appendChild(row);
    });
  }
  function renderPublication(scenario) {
    clear(els.problemPublication);
    const message = scenario.playable === false ? "尚未通过完整发布门禁，当前不能启动。" : scenario.publication_status ? `当前状态：${scenario.publication_status}` : "发布状态待验证。";
    els.problemPublication.appendChild(make("p", message));
    const receipt = scenario.publication_receipt || scenario.validation_receipt;
    if (receipt && typeof receipt === "object") Object.entries(receipt).forEach(([key, value]) => {
      const row = make("p"); row.append(make("strong", `${key}：`), document.createTextNode(typeof value === "object" ? JSON.stringify(value) : String(value))); els.problemPublication.appendChild(row);
    });
  }
  function renderProblem() {
    const scenario = state.selected;
    const mayRetryStart = state.pending?.uncertain && state.pending.action === "start";
    const playable = scenario?.playable !== false;
    els.startButton.disabled = RR_MODE || !scenario || !playable || state.capabilities?.available !== true || (!!state.pending && !mayRetryStart);
    els.problemFacts.hidden = !scenario;
    if (!scenario) return;
    const publication = scenario.publication_status ? ` · ${scenario.publication_status}` : "";
    els.scenarioMeta.textContent = `${array(scenario.tags).join(" · ") || "工程问题"} · v${displayValue(scenario.version, "?")}${publication}`;
    els.problemTitle.textContent = asText(scenario.title);
    els.problemSummary.textContent = asText(scenario.summary, "请依据现场信息完成诊断和修复。");
    els.problemSymptom.textContent = asText(scenario.symptom);
    els.problemGoal.textContent = asText(scenario.goal);
    clear(els.problemConstraints); array(scenario.constraints).forEach(addConstraint);
    if (!els.problemConstraints.childElementCount) addConstraint("待验证");
    renderProvenance(scenario.provenance);
    renderPublication(scenario);
    const same = state.current?.attempt?.scenario_id === scenario.id;
    els.startButton.textContent = !playable ? "等待发布验证" : mayRetryStart ? "重试开始并核对结果" : same && state.current.attempt.status === "active" ? "环境正在运行" : "开始这道题";
    els.startButton.disabled ||= same && state.current?.attempt?.status === "active";
    if (RR_MODE) els.startButton.textContent = "只读审核 · 请在本机练习";
  }
  function stepItem(step, index) {
    const li = make("li");
    li.appendChild(make("div", `${asText(step?.node, "当前节点")} · ${asText(step?.shell, "Shell待验证")} · 步骤 ${index + 1}`, "step-meta"));
    if (step?.command) li.appendChild(make("code", step.command));
    if (step?.expected) li.appendChild(make("p", `预期：${step.expected}`));
    if (step?.explanation) li.appendChild(make("p", `原因：${step.explanation}`));
    if (step?.recovery) li.appendChild(make("p", `偏离时：${step.recovery}`));
    return li;
  }
  function renderAssistance() {
    const scenario = state.selected;
    els.hintToggle.setAttribute("aria-pressed", String(state.hintOn));
    els.hintToggle.textContent = state.hintOn ? "提示常开" : "提示常关";
    els.hintsClosed.hidden = state.hintOn;
    els.hintsPanel.hidden = !state.hintOn;
    clear(els.hintSteps);
    if (state.hintOn && scenario) array(scenario.hints).forEach((step, index) => els.hintSteps.appendChild(stepItem(step, index)));
    const open = state.solutionOpen;
    els.solutionPanel.hidden = !open;
    els.solutionButton.setAttribute("aria-expanded", String(open));
    els.solutionButton.textContent = open ? "收起完整解答" : "查看完整解答";
    els.solutionButton.disabled = !scenario || !!state.pending;
    clear(els.solutionSteps);
    els.solutionExplanation.textContent = asText(scenario?.solution?.explanation, "暂无解答说明");
    if (open) array(scenario?.solution?.steps).forEach((step, index) => els.solutionSteps.appendChild(stepItem(step, index)));
  }
  function flattenEnvironment(environment) {
    if (!environment || typeof environment !== "object") return [];
    const labels = { adapter: "隔离方式", label: "环境", node: "当前节点", nodes: "节点", shell: "Shell", required_tools: "可用工具", tools: "可用工具", architecture: "架构", network: "网络", versions: "工具版本", workspace: "工作区" };
    return Object.entries(environment).flatMap(([key, value]) => {
      if (value === null || value === undefined) return [];
      if (key === "versions" || key === "label") return [];
      if (key === "limits" && typeof value === "object") {
        const mib = (bytes) => Number(bytes) < 1048576 ? `${Math.round(Number(bytes) / 1024)} KiB` : `${Math.round(Number(bytes) / 1048576)} MiB`;
        const values = [
          value.lifetime_seconds ? `最长 ${Math.round(Number(value.lifetime_seconds) / 60)} 分钟` : "",
          value.output_bytes ? `终端输出 ${mib(value.output_bytes)}` : "",
          value.workspace_bytes ? `工作区 ${mib(value.workspace_bytes)}` : "",
          value.workspace_entries ? `${value.workspace_entries} 个文件项` : "",
          value.per_process_memory_bytes ? `单进程内存 ${mib(value.per_process_memory_bytes)}` : "",
        ].filter(Boolean);
        return values.length ? [["资源边界", values.join(" · ")]] : [];
      }
      const shown = Array.isArray(value) ? value.join("、") : typeof value === "object" ? Object.entries(value).map(([name, version]) => `${name} ${version}`).join("、") : String(value);
      const translated = key === "adapter" && shown === "bwrap-userland" ? "Bubblewrap 用户态隔离" : key === "network" && shown === "isolated" ? "已隔离" : shown;
      return [[labels[key] || key.replaceAll("_", " "), translated]];
    });
  }
  function renderEnvironment() {
    clear(els.environmentFacts);
    const declared = scenarioById(state.current?.attempt?.scenario_id)?.environment || {};
    flattenEnvironment({ ...declared, ...(state.current?.environment || {}) }).forEach(([key, value]) => {
      const wrapper = make("div"); wrapper.append(make("dt", `${key}`), make("dd", value)); els.environmentFacts.appendChild(wrapper);
    });
  }
  function renderChecks() {
    clear(els.checksList);
    const checks = array(state.current?.attempt?.checks);
    els.checksEmpty.hidden = checks.length > 0;
    checks.forEach((check) => {
      const li = make("li");
      const infrastructureError = check.status === "infra_error";
      const ready = check.ready !== false && !infrastructureError;
      const passed = check.passed === true;
      const label = infrastructureError ? "平台检查错误" : !ready ? "平台尚未就绪" : passed ? "通过" : "未通过";
      li.appendChild(make("div", `${asText(check.name || check.id, "检查项")}：${label}`, `check-result ${passed ? "pass" : "fail"}`));
      if (check.evidence !== undefined) li.appendChild(make("p", `证据：${typeof check.evidence === "string" ? check.evidence : JSON.stringify(check.evidence)}`));
      if (check.details !== undefined) li.appendChild(make("p", `说明：${typeof check.details === "string" ? check.details : JSON.stringify(check.details)}`));
      if (check.message) li.appendChild(make("p", check.message));
      els.checksList.appendChild(li);
    });
  }
  function setTerminalActive(active) {
    els.ctrlCButton.disabled = !active || !!state.pending;
    els.reconnectButton.disabled = !state.current || active || !!state.pending;
    if (state.terminal) state.terminal.options.disableStdin = !active;
  }
  function renderAttempt() {
    const attempt = state.current?.attempt;
    els.labPanel.hidden = !attempt;
    if (!attempt) { $("problemPanel").appendChild(els.guideCard); renderProblem(); return; }
    els.labPanel.querySelector(".evidence").after(els.guideCard);
    const status = asText(attempt.status, "unknown");
    const active = status === "active" && !state.locateOnly;
    els.labHeading.textContent = `${asText(scenarioById(attempt.scenario_id)?.title, attempt.scenario_id)} · Attempt`;
    els.attemptStatus.textContent = ({active:"运行中",stopped:"已停止",lost:"已丢失",expired:"已过期"})[status] || status;
    els.attemptStatus.dataset.status = status;
    const different = state.selected && state.selected.id !== attempt.scenario_id;
    els.differentScenarioNotice.hidden = !different;
    if (different) els.differentScenarioNotice.textContent = "你正在查看另一道题。现有环境保持不变；只有明确开始新题才会停止它。";
    els.terminalTarget.textContent = active ? "已连接到一次性隔离环境" : "会话已结束；历史输出不会冒充实时终端回放";
    els.terminalMessage.textContent = active ? "终端输入会发送到当前 Attempt。" : "此 Attempt 已结束。你可以查看检查证据或重新开始。";
    setTerminalActive(active);
    const retryAction = state.pending?.uncertain ? state.pending.action : "";
    els.checkButton.disabled = !active || (!!state.pending && retryAction !== "check");
    els.stopButton.disabled = !active || (!!state.pending && retryAction !== "stop");
    els.resetButton.disabled = !attempt || (!!state.pending && retryAction !== "reset");
    els.checkButton.textContent = retryAction === "check" ? "重试检查并核对结果" : "检查修复结果";
    els.stopButton.textContent = retryAction === "stop" ? "重试停止并核对结果" : "停止环境";
    els.resetButton.textContent = retryAction === "reset" ? "重试重置并核对结果" : "重置环境";
    renderEnvironment(); renderChecks(); renderAssistance(); renderProblem(); renderArtifact();
  }
  function artifactNotice(kind, text) { state.artifactNotice = {kind, text}; }
  function renderArtifact() {
    const attempt = state.current?.attempt;
    const latest = array(attempt?.checks).at(-1);
    const selection = `${state.selected?.id || ""}:${attempt?.id || ""}`;
    const checkKey = JSON.stringify(latest || null);
    if (state.artifactSelection !== selection) {
      state.artifactNotice = null; state.artifactReceipt = null;
      // An uncertain export keeps its exact request until definitively resolved.
      state.artifactSelection = selection; state.artifactCheckKey = checkKey;
    } else if (state.artifactCheckKey !== checkKey) {
      state.artifactCheckKey = checkKey; state.artifactNotice = null; state.artifactReceipt = null;
    }
    const eligible = attempt?.status === "active" && attempt?.scenario_id === "media-wav-quality" && latest?.passed === true && !!latest?.artifact_binding;
    els.exportWavButton.disabled = RR_MODE || !eligible || state.artifactPending || !!state.pending;
    const receipt = state.artifactReceipt;
    const same = receipt?.binding?.attempt_id === attempt?.id;
    els.downloadWavButton.disabled = !same || !eligible || state.artifactPending;
    if (state.artifactNotice) {
      els.artifactState.textContent = state.artifactNotice.text;
      els.artifactState.dataset.status = state.artifactNotice.kind;
    } else {
      els.artifactState.dataset.status = "idle";
      els.artifactState.textContent = attempt?.status !== "active" ? "环境已结束：旧产物引用失效，已导出的文件与记录保留。" : "仅最新 WAV 检查通过且字节未改变时可导出。";
    }
    if (!same || !eligible) els.artifactProvenance.textContent = "";
  }
  function artifactFacts(artifact) {
    return `SHA256：${artifact.sha256}\n大小：${artifact.size} 字节\n采样率：${artifact.sample_rate_hz} Hz · 声道：${artifact.channels}\n样本宽度：${artifact.sample_width_bytes} 字节 · 帧数：${artifact.frames}\n时长：${artifact.duration_seconds} 秒`;
  }
  async function exportWav() {
    const id = state.current?.attempt?.id;
    if (!id || state.artifactPending) return;
    state.artifactPending = true; artifactNotice("loading", "正在核对检查版本与 WAV 字节…"); renderArtifact();
    try {
      if (!state.artifactOperation || state.artifactOperation.attempt !== id) {
        const binding = await request(`/api/lab/attempts/${id}/wav`);
        state.artifactOperation = {attempt: id, operation_id: operationId(), binding};
      }
      const pending = state.artifactOperation;
      const receipt = await request(`/api/lab/attempts/${id}/export-wav`, {method: "POST", body: JSON.stringify({operation_id: pending.operation_id, binding: pending.binding})});
      if (state.current?.attempt?.id !== id) return;
      state.artifactReceipt = receipt; state.artifactOperation = null;
      els.artifactProvenance.textContent = artifactFacts(receipt.binding.artifact);
      artifactNotice("success", "已导出并核对 SHA256 与 WAV 参数。未作听觉或掌握度判断。");
    } catch (error) {
      if (state.current?.attempt?.id !== id) return;
      if (error.definitive) { state.artifactOperation = null; state.artifactReceipt = null; }
      const stale = error.status === 409 || error.status === 410;
      artifactNotice(stale ? "stale" : "error", `导出未完成：${error.message}。${stale ? "请重新检查修复结果，再核对并导出。" : error.definitive ? "修正问题后可重新核对。" : "结果不确定；再次点击将用同一请求核对。"}`);
    } finally { state.artifactPending = false; renderArtifact(); }
  }
  async function downloadWav() {
    const receipt = state.artifactReceipt;
    if (!receipt || state.artifactPending) return;
    state.artifactPending = true; artifactNotice("loading", "正在核对下载字节…"); renderArtifact();
    try {
      const response = await fetch(receipt.download_url, {headers: {"X-Lab-Token": state.token}});
      if (!response.ok) { const error = new Error(`产物引用失效或下载失败（${response.status}）`); error.status = response.status; throw error; }
      const blob = await response.blob();
      if (blob.size !== receipt.binding.artifact.size || blob.size > 64000) throw new Error("下载长度不符");
      const hash = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", await blob.arrayBuffer()))).map(x => x.toString(16).padStart(2, "0")).join("");
      if (hash !== receipt.binding.artifact.sha256) throw new Error("下载摘要不符");
      const url = URL.createObjectURL(blob); const link = make("a");
      link.href = url; link.download = "tone.wav"; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
      artifactNotice("success", "下载完成，SHA256 已核对。");
    } catch (error) { artifactNotice(error.status === 409 || error.status === 410 ? "stale" : "error", error.message); state.artifactReceipt = null; if (error.status === 409 || error.status === 410) state.artifactOperation = null; }
    finally { state.artifactPending = false; renderArtifact(); }
  }
  function enqueueInput(data) {
    if (!data || state.inputUncertain || state.current?.attempt?.status !== "active") return;
    let chunk = "";
    for (const character of Array.from(data)) {
      if (chunk && new TextEncoder().encode(chunk + character).length > 2048) { state.inputQueue.push(chunk); chunk = ""; }
      chunk += character;
    }
    if (chunk) state.inputQueue.push(chunk);
    clearTimeout(state.inputTimer);
    state.inputTimer = setTimeout(() => drainInput(), 18);
  }
  async function drainInput() {
    clearTimeout(state.inputTimer);
    if (state.inputDrain) return state.inputDrain;
    state.inputDrain = (async () => {
      while (state.inputQueue.length && !state.inputUncertain) {
        const attemptId = state.current?.attempt?.id;
        if (!attemptId || state.current.attempt.status !== "active") { state.inputQueue.length = 0; break; }
        let data = state.inputQueue.shift();
        while (state.inputQueue.length && new TextEncoder().encode(data + state.inputQueue[0]).length <= 2048) data += state.inputQueue.shift();
        const generation = state.generation; const operation = operationId();
        try {
          const snapshot = await request(`/api/lab/attempts/${encodeURIComponent(attemptId)}/input`, { method: "POST", body: JSON.stringify({ data, operation_id: operation }) });
          if (generation === state.generation && state.current?.attempt?.id === attemptId) applySnapshot(snapshot);
        } catch (error) {
          state.inputUncertain = { attemptId, operation, data };
          els.terminalMessage.textContent = `终端输入结果暂不确定：${error.message}。输入已暂停，不会自动重发；请重新连接核对现场。`;
          setTerminalActive(false); els.reconnectButton.disabled = false;
        }
      }
    })();
    try { await state.inputDrain; } finally { state.inputDrain = null; }
  }
  async function flushInput() {
    clearTimeout(state.inputTimer);
    await drainInput();
    if (state.inputUncertain) {
      els.operationState.textContent = "终端输入结果尚未核对，暂不执行环境操作。请先重新连接。";
      return false;
    }
    return true;
  }
  function cancelResize() {
    clearTimeout(state.fitTimer); state.fitTimer = 0;
    if (state.resizeAbortController) state.resizeAbortController.abort();
    state.resizeAbortController = null;
  }
  function scheduleResize() {
    cancelResize();
    const attemptId = state.current?.attempt?.id;
    const generation = state.generation;
    if (!attemptId || state.current.attempt.status !== "active" || state.pending || !state.terminal) return;
    state.fitTimer = setTimeout(async () => {
      state.fitTimer = 0;
      if (generation !== state.generation || state.current?.attempt?.id !== attemptId || state.current.attempt.status !== "active" || state.pending) return;
      const cols = Math.max(20, Math.floor(els.terminal.clientWidth / 9));
      const rows = Math.max(8, Math.floor(els.terminal.clientHeight / 18));
      const resizeKey = `${generation}:${attemptId}:${cols}:${rows}`;
      if (state.lastResizeKey === resizeKey) return;
      state.lastResizeKey = resizeKey;
      state.terminal.resize(cols, rows);
      const controller = new AbortController(); state.resizeAbortController = controller;
      try {
        const snapshot = await request(`/api/lab/attempts/${encodeURIComponent(attemptId)}/resize`, { method: "POST", body: JSON.stringify({ cols, rows }), signal: controller.signal });
        if (!controller.signal.aborted && generation === state.generation && state.current?.attempt?.id === attemptId && state.current.attempt.status === "active" && !state.pending) applySnapshot(snapshot);
      } catch (error) {
        if (error.name !== "AbortError" && generation === state.generation && state.current?.attempt?.id === attemptId && state.current.attempt.status === "active" && !state.pending) {
          els.terminalMessage.textContent = `终端尺寸同步失败：${error.message}。终端仍可继续使用。`;
        }
      } finally {
        if (state.resizeAbortController === controller) state.resizeAbortController = null;
      }
    }, 120);
  }
  function ensureTerminal() {
    if (state.terminal || typeof window.Terminal !== "function") {
      if (!state.terminal && typeof window.Terminal !== "function") {
        els.terminalMessage.textContent = "终端组件未加载。请检查本地 vendor/xterm 文件。";
      }
      return;
    }
    state.terminal = new window.Terminal({ cursorBlink: true, convertEol: true, fontSize: 14, scrollback: 3000, theme: { background: "#0b0b0e", foreground: "#f7f0e8", cursor: "#d49a70", selectionBackground: "#5f526f" } });
    state.terminal.open(els.terminal);
    state.terminal.onData((data) => enqueueInput(data));
    new ResizeObserver(() => scheduleResize()).observe(els.terminal);
  }
  function applySnapshot(snapshot, { restoring = false } = {}) {
    if (!snapshot?.attempt?.id) throw new Error("服务返回的 Attempt 快照不完整");
    const revision = Number(snapshot.revision);
    const knownRevision = state.revisions.get(snapshot.attempt.id);
    if (Number.isFinite(revision) && Number.isFinite(knownRevision) && revision < knownRevision) return false;
    if (Number.isFinite(revision)) state.revisions.set(snapshot.attempt.id, revision);
    const previousId = state.current?.attempt?.id;
    const previousStatus = state.current?.attempt?.status;
    const previousCursor = state.cursor;
    state.current = snapshot;
    const nextCursor = Number.isInteger(snapshot.cursor) ? snapshot.cursor : previousCursor;
    state.cursor = nextCursor;
    rememberAttempt(snapshot.attempt);
    ensureTerminal();
    if (state.terminal && previousId !== snapshot.attempt.id) state.terminal.clear();
    if (state.terminal && snapshot.attempt.status === "active" && snapshot.output) {
      const characters = Array.from(String(snapshot.output));
      const outputBase = Math.max(0, nextCursor - characters.length);
      const start = previousId === snapshot.attempt.id ? Math.max(0, previousCursor - outputBase) : 0;
      if (start < characters.length) state.terminal.write(characters.slice(start).join(""));
    }
    if (restoring && snapshot.attempt.status !== "active" && state.terminal) state.terminal.clear();
    renderAttempt();
    if (snapshot.attempt.status === "active") schedulePoll(); else clearTimeout(state.pollTimer);
    if (previousStatus === "active" && snapshot.attempt.status !== "active") els.terminalMessage.textContent = "会话已经结束；终端已切换为只读状态。";
    setUrl(state.selected?.id || snapshot.attempt.scenario_id,
      state.selected?.id === snapshot.attempt.scenario_id ? snapshot.attempt.id : null, "replace");
    if (snapshot.attempt.status === "active" && !state.pending) scheduleResize();
    return true;
  }
  async function loadAttempt(id, { restoring = true } = {}) {
    abortRequests(); const generation = state.generation;
    els.operationState.textContent = "正在连接 Attempt…";
    try {
      const snapshot = await request(`/api/lab/attempts/${encodeURIComponent(id)}?cursor=0`, { signal: state.controller.signal });
      if (generation !== state.generation) return;
      applySnapshot(snapshot, { restoring }); state.inputUncertain = null; els.operationState.textContent = ""; drainInput();
    } catch (error) {
      if (error.name === "AbortError") return;
      if (generation !== state.generation) return;
      els.operationState.textContent = `无法连接 Attempt：${error.message}`;
      setUrl(state.selected?.id, null, "replace");
    }
  }
  function schedulePoll() {
    clearTimeout(state.pollTimer);
    if (state.current?.attempt?.status !== "active") return;
    const attemptId = state.current.attempt.id;
    const generation = state.generation;
    state.pollTimer = setTimeout(async () => {
      try {
        const snapshot = await request(`/api/lab/attempts/${encodeURIComponent(attemptId)}?cursor=${state.cursor}`);
        if (generation !== state.generation || state.current?.attempt?.id !== attemptId) return;
        applySnapshot(snapshot);
      } catch (error) {
        if (generation !== state.generation) return;
        els.terminalMessage.textContent = `实时连接中断：${error.message}。可使用“重新连接”。`;
        els.reconnectButton.disabled = false;
      }
    }, POLL_MS);
  }
  function pendingKey(action, payload) { return `${state.current?.attempt?.id || state.selected?.id || "none"}:${action}:${JSON.stringify(payload)}`; }
  async function mutate(action, data = {}, options = {}) {
    if (RR_MODE) return null;
    if (state.pending && !options.quiet && !state.pending.uncertain) return;
    const start = action === "start";
    const payload = { ...data };
    const key = pendingKey(action, payload);
    let operation = state.pending?.key === key && state.pending?.uncertain ? state.pending.operation : operationId();
    if (!new Set(["resize", "view"]).has(action)) payload.operation_id = operation;
    const path = start ? "/api/lab/start" : `/api/lab/attempts/${encodeURIComponent(state.current.attempt.id)}/${action}`;
    const targetAttempt = state.current?.attempt?.id || null;
    const generation = options.quiet ? state.generation : state.generation + 1;
    if (!options.quiet) { cancelResize(); state.generation = generation; clearTimeout(state.pollTimer); }
    if (!options.quiet) {
      state.pending = { key, operation, uncertain: false, action };
      els.operationState.textContent = action === "check" ? "正在从隔离环境取证…" : "操作进行中…";
      renderAttempt();
    }
    try {
      const snapshot = await request(path, { method: "POST", body: JSON.stringify(payload) });
      if (!options.quiet) state.pending = null;
      const stillCurrent = generation === state.generation && (start || state.current?.attempt?.id === targetAttempt);
      if (stillCurrent) applySnapshot(snapshot);
      els.operationState.textContent = action === "check" ? "检查完成。结论以下方证据为准。" : "操作已完成。";
      if (start) { state.selected = scenarioById(snapshot.attempt.scenario_id) || state.selected; renderCatalog(); }
      return snapshot;
    } catch (error) {
      if (!options.quiet) {
        if (error.definitive) state.pending = null;
        else state.pending = { key, operation, uncertain: true, action };
        els.operationState.textContent = `${error.message}${error.definitive ? "" : "。结果暂不确定；重试会使用同一操作编号核对结果。"}`;
        renderAttempt();
        if (state.current?.attempt?.status === "active") schedulePoll();
        if (!state.pending && state.current?.attempt?.status === "active") scheduleResize();
      }
      return null;
    }
  }
  async function recordAssistanceForCurrent() {
    const scenarioId = state.current?.attempt?.scenario_id;
    const exposure = scenarioId ? state.preViewed[scenarioId] || {} : {};
    if (exposure.hints) await mutate("view", { kind: "hints" }, { quiet: true });
    if (exposure.solution) await mutate("view", { kind: "solution" }, { quiet: true });
  }
  async function startSelected() {
    state.locateOnly = false;
    if (!state.selected) return;
    cancelResize();
    const otherActive = state.current?.attempt?.status === "active" && state.current.attempt.scenario_id !== state.selected.id;
    if (otherActive && !window.confirm("开始新题会停止当前正在运行的另一道题环境，并保留它的 Attempt 记录。继续吗？")) return;
    if (!await flushInput()) return;
    const scenarioId = state.selected.id;
    abortRequests(); state.current = null; state.cursor = 0;
    state.inputQueue.length = 0; state.inputUncertain = null;
    if (state.terminal) state.terminal.clear();
    await mutate("start", { scenario_id: scenarioId });
    if (state.current) await recordAssistanceForCurrent();
    await loadHistory();
  }
  async function selectScenario(id, { historyMode = "replace", attemptId = null, loadRemembered = false } = {}) {
    abortRequests();
    if (id && !scenarioById(id)) { showError("题目不存在或链接已失效。"); return; }
    if (attemptId && !/^[A-Za-z0-9_-]{1,80}$/.test(attemptId)) { showError("Attempt 链接无效。"); return; }
    const scenario = scenarioById(id) || state.scenarios[0] || null;
    if (!scenario) return;
    if (state.selected?.id !== scenario.id) state.solutionOpen = false;
    state.selected = scenario; renderCatalog(); renderProblem(); renderAssistance();
    if (state.hintOn && !state.locateOnly) state.preViewed[scenario.id] = { ...(state.preViewed[scenario.id] || {}), hints: true };
    const mapped = loadRemembered ? attemptMap()[scenario.id] : null;
    const wanted = RR_MODE ? null : (attemptId || mapped);
    setUrl(scenario.id, wanted, historyMode);
    if (state.locateOnly) {
      state.hintOn = false; state.solutionOpen = false;
      const query = new URLSearchParams({scenario: scenario.id}); if (wanted) query.set("attempt", wanted);
      try {
        const found = await request(`/api/lab/locate?${query}`);
        state.current = found.attempt ? {attempt: found.attempt, output: "", environment: {}, cursor: 0} : null;
        renderAttempt(); renderAssistance();
        if (found.attempt) { els.reconnectButton.disabled = false; els.reconnectButton.textContent = "连接此环境"; }
      } catch (error) { showError(`定位失败：${error.message}`); }
    } else if (wanted && state.current?.attempt?.id !== wanted) await loadAttempt(wanted);
    else {
      renderAttempt();
      if (state.current?.attempt?.status === "active") { schedulePoll(); scheduleResize(); }
    }
    els.problemTitle.focus({ preventScroll: true });
  }
  async function loadHistory() {
    if (RR_MODE) {
      clear(els.attemptHistory); els.historyStatus.hidden = false;
      els.historyStatus.textContent = "本次审核不开放个人尝试记录，请在本机查看。";
      return;
    }
    els.historyStatus.textContent = "正在读取…";
    try {
      const data = await request("/api/lab/history"); state.attempts = array(data.attempts);
      clear(els.attemptHistory); els.historyStatus.hidden = state.attempts.length > 0;
      els.historyStatus.textContent = "还没有练习记录。";
      state.attempts.forEach((attempt) => {
        const li = make("li"); const button = make("button"); button.type = "button";
        const scenario = scenarioById(attempt.scenario_id);
        const checks = array(attempt.checks);
        const validChecks = checks.filter((check) => check.ready !== false && check.status !== "infra_error" && typeof check.passed === "boolean");
        const latest = validChecks.length ? validChecks[validChecks.length - 1] : null;
        const hadPass = validChecks.some((check) => check.passed === true);
        const evidence = latest?.passed ? "最近有效检查通过" : hadPass ? "最近检查未通过，曾有通过证据" : latest ? "最近有效检查未通过" : "暂无有效检查证据";
        const assistance = [attempt.hints_viewed ? "看过提示" : "", attempt.solution_viewed ? "看过解答" : ""].filter(Boolean).join("、") || "未查看辅助";
        button.append(make("strong", asText(scenario?.title, attempt.scenario_id)), make("small", `${asText(attempt.status)} · ${evidence} · ${assistance} · ${asText(attempt.started_at || attempt.created_at, "时间待验证")}`));
        button.addEventListener("click", () => selectScenario(attempt.scenario_id, { historyMode: "push", attemptId: attempt.id }));
        li.appendChild(button); els.attemptHistory.appendChild(li);
      });
    } catch (error) { els.historyStatus.hidden = false; els.historyStatus.textContent = `历史读取失败：${error.message}`; }
  }
  async function bootstrap() {
    showError("");
    try {
      const data = await request("/api/lab/bootstrap");
      state.token = asText(data.token, ""); state.capabilities = data.capabilities || {}; state.scenarios = array(data.scenarios);
      if (!RR_MODE && !state.token) throw new Error("本地服务没有提供会话令牌");
      if (RR_MODE) {
        window.CSP_RR_CONTEXT = { source: data.source, resource: data.resource };
        const legacy = document.querySelector('a[href="progress.html"]'); if (legacy) legacy.remove();
        const stylesheet = document.createElement("link"); stylesheet.rel = "stylesheet"; stylesheet.href = "/rr_feedback.css"; document.head.append(stylesheet);
        const feedback = document.createElement("script"); feedback.src = "/rr_feedback.js"; document.head.append(feedback);
      }
      capabilitySummary(); renderFilters(); renderCatalog(); if (!state.locateOnly) await loadHistory();
      const params = new URLSearchParams(location.search);
      if (["scenario", "attempt", "locate"].some(key => params.getAll(key).length > 1) || (params.has("locate") && params.get("locate") !== "1")) throw new Error("定位参数无效或重复");
      const requestedScenario = params.get("scenario"); const requestedAttempt = params.get("attempt");
      await selectScenario(requestedScenario, { attemptId: requestedAttempt, loadRemembered: !requestedAttempt });
    } catch (error) {
      els.catalogStatus.textContent = "本机题库载入失败。"; showError(`无法打开练习工作台：${error.message}。请确认本地服务正在运行后重试。`);
    }
  }

  els.scenarioSearch.addEventListener("input", (event) => { state.query = event.target.value; renderCatalog(); });
  els.hintToggle.addEventListener("click", async () => {
    state.hintOn = !state.hintOn; localStorage.setItem(HINT_KEY, state.hintOn ? "on" : "off"); renderAssistance();
    if (state.hintOn && state.selected) state.preViewed[state.selected.id] = { ...(state.preViewed[state.selected.id] || {}), hints: true };
    if (state.current?.attempt?.scenario_id === state.selected?.id && state.hintOn) await mutate("view", { kind: "hints" }, { quiet: true });
  });
  els.exportWavButton.addEventListener("click", exportWav);
  els.downloadWavButton.addEventListener("click", downloadWav);
  els.startButton.addEventListener("click", startSelected);
  els.checkButton.addEventListener("click", async () => { cancelResize(); if (await flushInput()) { await mutate("check"); await loadHistory(); } });
  els.stopButton.addEventListener("click", async () => { cancelResize(); if (await flushInput()) { await mutate("stop"); await loadHistory(); } });
  els.resetButton.addEventListener("click", () => els.resetDialog.showModal());
  els.resetDialog.addEventListener("close", async () => { if (els.resetDialog.returnValue === "confirm") { cancelResize(); if (await flushInput()) { const snapshot = await mutate("reset"); if (snapshot) await recordAssistanceForCurrent(); await loadHistory(); } } });
  els.solutionButton.addEventListener("click", async () => {
    if (state.solutionOpen) { state.solutionOpen = false; renderAssistance(); return; }
    if (!state.selected) return;
    state.preViewed[state.selected.id] = { ...(state.preViewed[state.selected.id] || {}), solution: true };
    if (state.current?.attempt?.scenario_id === state.selected.id) await mutate("view", { kind: "solution" }, { quiet: true });
    state.solutionOpen = true;
    renderAssistance();
  });
  els.ctrlCButton.addEventListener("click", () => enqueueInput("\u0003"));
  els.reconnectButton.addEventListener("click", () => { state.locateOnly = false; return state.current && loadAttempt(state.current.attempt.id); });
  els.refreshHistory.addEventListener("click", loadHistory);
  window.addEventListener("popstate", async () => {
    const params = new URLSearchParams(location.search);
    await selectScenario(params.get("scenario"), { attemptId: params.get("attempt"), historyMode: "replace" });
  });
  document.addEventListener("visibilitychange", () => { if (!state.locateOnly && !document.hidden && state.current?.attempt?.status === "active") loadAttempt(state.current.attempt.id); });
  renderAssistance(); bootstrap();
})();
