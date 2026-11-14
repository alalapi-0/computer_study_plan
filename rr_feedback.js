"use strict";
(() => {
  if (location.origin !== "https://rr-computer-study-plan.invalid:9419") return;
  const context = window.CSP_RR_CONTEXT;
  const mount = document.getElementById("rrFeedbackMount");
  if (!context || !mount) return;
  mount.className = "rr-feedback"; mount.hidden = false;
  function node(tag, text, attributes = {}) {
    const element = document.createElement(tag);
    if (text !== null) element.textContent = text;
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
    return element;
  }
  const heading = node("h2", "反馈这次审核", { id: "rrFeedbackHeading" });
  mount.setAttribute("aria-labelledby", heading.id);
  mount.append(heading, node("p", "这是实际工作台的只读审核。终端和实验操作请在本机使用。提交前请检查正文与附件，避免包含密码或私人信息。"));
  const form = node("form", null);
  const fields = node("fieldset", null);
  function area(label, name, required = false) {
    const wrapper = node("label", label);
    const input = node("textarea", null, { name, id: "rr-" + name, maxlength: "7000" });
    input.required = required; wrapper.append(input); fields.append(wrapper);
    return input;
  }
  const description = area("问题描述（必填）", "description", true);
  const expected = area("预期表现", "expected");
  const actual = area("实际表现", "actual");
  const steps = area("重现步骤", "steps");
  const fileLabel = node("label", "附件（可选，最多两件，每件不超过 1 MiB）");
  const files = node("input", null, { type: "file", multiple: "", accept: "image/png,image/jpeg,image/webp,text/plain", id: "rr-files" });
  fileLabel.append(files, node("small", "支持 PNG、JPEG、WebP 或 UTF-8 文本；图片不超过 400 万像素。")); fields.append(fileLabel);
  const checkLabel = node("label", null, { class: "rr-review-check" });
  const consent = node("input", null, { type: "checkbox", required: "", id: "rr-consent" });
  checkLabel.append(consent, node("span", "我已检查正文与附件，确认可以提交。")); fields.append(checkLabel);
  const actions = node("div", null, { class: "rr-actions" });
  const submit = node("button", "提交反馈", { type: "submit", class: "primary" });
  const fresh = node("button", "新建反馈", { type: "button" }); fresh.hidden = true;
  actions.append(submit, fresh); form.append(fields, actions);
  const status = node("output", "未同步：填写并检查后提交。", { id: "rrFeedbackStatus", role: "status", "aria-live": "polite" });
  mount.append(form, status);
  const query = node("form", null, { class: "rr-query" });
  const queryLabel = node("label", "查询已提交反馈");
  const queryId = node("input", null, { type: "text", id: "rr-query-id", autocomplete: "off", placeholder: "反馈编号", required: "" });
  const queryButton = node("button", "刷新处理状态", { type: "submit" });
  queryLabel.append(queryId); query.append(queryLabel, queryButton); mount.append(query);
  let pending = null, sending = false, accepted = false;
  async function sha(bytes) {
    const hash = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2, "0")).join("");
  }
  async function fetchJSON(path, options = {}) {
    const response = await fetch(path, { cache: "no-store", ...options });
    const value = await response.json();
    if (!response.ok) {
      const reasons = { 400: "正文或附件格式有误", 413: "正文或附件超过大小限制", 415: "附件无法读取，请使用符合要求的图片或 UTF-8 文本", 409: "请求内容或来源版本不一致" };
      const error = new Error(reasons[response.status] || "请求未完成"); error.status = response.status; throw error;
    }
    return value;
  }
  function render(record) {
    const labels = { pending: "持久保存，待 Agent 读取", agent_read: "Agent 已读", processed: "已处理" };
    if (!labels[record.state] || !record.feedback_id || !Number.isInteger(record.revision)) throw new Error("回执不完整");
    status.textContent = labels[record.state] + "。反馈编号：" + record.feedback_id;
    if (record.result?.summary) status.textContent += "。处理说明：" + record.result.summary;
    if (record.payload?.source && JSON.stringify(record.payload.source) !== JSON.stringify(context.source)) status.textContent += "。这条反馈来自此前版本。";
    queryId.value = record.feedback_id;
  }
  async function showFeedback(id) {
    if (!/^[a-f0-9-]{36}$/.test(id)) throw new Error("编号格式不正确");
    const record = await fetchJSON("/__rr/v1/feedback/" + id);
    render(record); return record;
  }
  function ordered(value) {
    if (Array.isArray(value)) return value.map(ordered);
    if (value && typeof value === "object") return Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])]));
    return value;
  }
  async function prepare() {
    const chosen = Array.from(files.files);
    if (chosen.length > 2) throw new Error("最多选择两件附件。");
    const blobs = [], attachments = [];
    for (const file of chosen) {
      if (file.size > 1048576) throw new Error("每件附件不能超过 1 MiB。");
      const type = file.type || (file.name.endsWith(".txt") ? "text/plain" : "");
      if (!["image/png", "image/jpeg", "image/webp", "text/plain"].includes(type)) throw new Error("附件仅支持 PNG、JPEG、WebP 或 UTF-8 文本。");
      const bytes = await file.arrayBuffer();
      attachments.push({ attachment_id: crypto.randomUUID(), size: bytes.byteLength, sha256: await sha(bytes) });
      blobs.push(new Blob([bytes], { type }));
    }
    const payload = { schema: 1, client_request_id: crypto.randomUUID(), project_id: "computer-study-plan",
      page_path: "/", source: context.source, resource: context.resource,
      description: description.value, expected: expected.value, actual: actual.value, steps: steps.value,
      submitted_at: new Date().toISOString(), attachments };
    const raw = JSON.stringify(payload);
    if (new TextEncoder().encode(raw).length > 16384) throw new Error("正文过长，请缩短后提交。");
    return { payload, raw, blobs, payload_sha256: await sha(new TextEncoder().encode(JSON.stringify(ordered(payload)))), attempted: false };
  }
  form.addEventListener("submit", async event => {
    event.preventDefault(); if (sending || accepted) return;
    sending = true; fields.disabled = true; submit.disabled = true; fresh.disabled = true;
    try {
      pending ||= await prepare();
      const path = "/__rr/v1/feedback/by-request/" + pending.payload.client_request_id;
      if (pending.attempted) {
        status.textContent = "同步中：先核对上次提交结果…";
        try {
          const receipt = await fetchJSON(path);
          await showFeedback(receipt.feedback_id); accepted = true; fresh.hidden = false; return;
        } catch (error) { if (error.status !== 404) throw error; }
      }
      status.textContent = "同步中：正在请求项目持久保存…";
      const body = new FormData();
      body.append("feedback", new Blob([pending.raw], { type: "application/json" }), "feedback.json");
      pending.blobs.forEach((blob, index) => body.append("attachment." + index, blob, "attachment"));
      pending.attempted = true;
      const receipt = await fetchJSON("/__rr/v1/feedback", { method: "POST", body });
      if (receipt.project_id !== pending.payload.project_id || receipt.client_request_id !== pending.payload.client_request_id
          || receipt.payload_sha256 !== pending.payload_sha256 || !receipt.accepted_at || !Number.isInteger(receipt.revision)
          || !Array.isArray(receipt.attachments) || receipt.attachments.length !== pending.payload.attachments.length
          || receipt.attachments.some((item, index) => ["attachment_id", "size", "sha256"].some(key => item[key] !== pending.payload.attachments[index][key]))) throw new Error("持久回执未核实");
      accepted = true; fresh.hidden = false; queryId.value = receipt.feedback_id;
      status.textContent = "持久保存，待 Agent 读取。反馈编号：" + receipt.feedback_id;
    } catch (error) {
      if ([400, 413, 415].includes(error.status)) {
        pending = null; status.textContent = "未同步：" + error.message + "。已保留填写内容，请修改后重新提交。";
      } else {
        status.textContent = pending?.attempted ? "失败待核对：提交结果尚未确认。再次提交会先查询同一请求，不会另建反馈。" : "未同步：" + error.message;
      }
    } finally {
      sending = false; fields.disabled = accepted || !!pending?.attempted;
      submit.disabled = accepted; fresh.disabled = false; fresh.hidden = !pending;
      submit.textContent = pending?.attempted && !accepted ? "核对并继续提交" : "提交反馈";
    }
  });
  fresh.addEventListener("click", () => {
    pending = null; accepted = false; fields.disabled = false; submit.disabled = false; fresh.hidden = true; form.reset();
    status.textContent = "未同步：填写并检查后提交。"; description.focus();
  });
  query.addEventListener("submit", async event => {
    event.preventDefault(); queryButton.disabled = true; status.textContent = "同步中：正在读取处理状态…";
    try { await showFeedback(queryId.value.trim()); }
    catch (_) { status.textContent = "失败待核对：暂时无法确认这条反馈，请核对编号后重试。"; }
    finally { queryButton.disabled = false; }
  });
})();
