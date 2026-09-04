/* SkyWays Architect · site frame.
   Layered onto the tool at build time by site/build.py. It adds attribution, the licence notice and
   disclaimer, the invitation to the ideas thread, and a contact form. Everything it creates is appended
   to the end of <body> with an "sw-" prefix; it never reads or changes the tool's own DOM or state. */
(function () {
  "use strict";
  var cfg = window.SKYWAYS_SITE || {};
  var links = cfg.links || {};
  var contact = cfg.contact || {};
  var author = cfg.author || "Akash Das";
  var year = cfg.year || new Date().getFullYear();

  function h(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "html") node.innerHTML = attrs[k];
      else if (k.indexOf("on") === 0) node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (kid) {
      node.appendChild(typeof kid === "string" ? document.createTextNode(kid) : kid);
    });
    return node;
  }
  function address() { return (contact.mailto || []).join("@"); }
  function a(href, text) { return '<a href="' + href + '" target="_blank" rel="noopener">' + text + "</a>"; }

  function mailtoHref(d) {
    var subject = "[SkyWays Architect] " + (d.topic || "message") + " from " + (d.name || "a visitor");
    var body = (d.message || "") + "\n\n-- \n" + (d.name || "") + (d.email ? " <" + d.email + ">" : "") +
      "\nsent from " + location.href;
    return "mailto:" + address() + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  }

  /* ---------- footer: attribution, licence, disclaimer, invitation ---------- */
  function footer() {
    var f = h("footer", { "class": "sw-footer", id: "sw-about", "aria-label": "About this site" });
    f.innerHTML =
      '<div class="sw-wrap">' +
      "<section><h2>About this tool</h2>" +
      '<p><span class="sw-name">SkyWays Architect</span> is an original work and the intellectual property of ' +
      '<span class="sw-name">' + author + "</span>. It is open-sourced under the " + a(links.license, "MIT Licence") +
      " for knowledge and experience sharing: study it, fork it, teach with it, and keep the copyright notice and " +
      "attribution when you reuse any part of it.</p>" +
      '<div class="sw-notice"><b>Disclaimer.</b> SkyWays is a fictional airline. Every figure, benchmark and price in ' +
      "the walk-through is illustrative and dated to when it was written; check it against your own numbers before " +
      "you decide anything. This site is not affiliated with, sponsored by or endorsed by Amazon Web Services or any " +
      "airline, and is provided as is, without warranty of any kind.</div></section>" +
      "<section><h2>Pitch in</h2>" +
      "<p>Have an idea, a disagreement, or a scenario the simulator gets wrong? Every suggestion is read, and the " +
      "ones that ship are credited.</p><ul>" +
      "<li>" + a(links.ideas, "Pitch an idea in the discussion thread") + "</li>" +
      "<li>" + a(links.discussions, "Browse all discussions") + "</li>" +
      "<li>" + a(links.issues, "Report a problem") + "</li>" +
      "<li>" + a(links.repo, "Star or fork the repository") + "</li></ul></section>" +
      "<section><h2>Contact</h2>" +
      "<p>Prefer a quiet word? Write to me directly. Messages arrive by e-mail and are kept privately; nothing " +
      "you send here is published.</p>" +
      '<button class="sw-btn" type="button" data-sw-open>&#9993;&#xFE0E; Write to ' + author.split(" ")[0] + "</button></section>" +
      '<div class="sw-legal"><span>&copy; ' + year + " " + author + "</span>" + a(links.license, "MIT Licence") +
      a(links.source, "Source") + '<a href="' + (links.frameless || "#") + '">Frameless version</a>' +
      a(links.repo, "Part of Agentic AI on AWS") + "</div></div>";
    return f;
  }

  /* ---------- drawer: the contact form ---------- */
  var scrim, drawer, form, sendBtn, status, opener = null;

  function field(label, control) {
    return h("div", { "class": "sw-field" }, [h("label", { "for": control.id, text: label }), control]);
  }
  function setStatus(kind, nodes) {
    status.className = "sw-status on " + kind;
    status.innerHTML = "";
    nodes.forEach(function (n) { status.appendChild(typeof n === "string" ? document.createTextNode(n) : n); });
  }
  function collect() {
    var d = {};
    ["name", "email", "topic", "message", "website"].forEach(function (k) { d[k] = (form.elements[k].value || "").trim(); });
    return d;
  }
  function mailLink(d, text) {
    return h("a", { href: mailtoHref(d), text: text || "open your mail app" });
  }

  function submit(e) {
    e.preventDefault();
    var d = collect();
    if (d.website) { setStatus("ok", ["Thank you."]); return; }            // honeypot: bots only
    if (!contact.endpoint) {                                                  // no relay configured: mail app
      location.href = mailtoHref(d);
      setStatus("ok", ["Your mail app should now have the message ready to send. If nothing opened, write to ",
        h("b", { text: address() }), " or ", mailLink(d, "try again"), "."]);
      return;
    }
    var body = { name: d.name, email: d.email, topic: d.topic, message: d.message,
      page: location.pathname + location.hash, website: "",
      _subject: "[SkyWays Architect] " + d.topic + " from " + d.name };
    if (contact.accessKey) body.access_key = contact.accessKey;
    sendBtn.disabled = true;
    setStatus("", ["Sending…"]);
    fetch(contact.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { r: r, j: j }; });
    }).then(function (x) {
      if (x.r.status === 429) throw new Error(x.j.error || "too many messages from this network right now; try again in ten minutes");
      if (!x.r.ok || x.j.ok === false || x.j.success === false) throw new Error(x.j.error || x.j.message || ("HTTP " + x.r.status));
      form.reset();
      setStatus("ok", ["Sent. Thank you — every message is read, and the ones that need a reply get one."]);
    }).catch(function (err) {
      setStatus("err", ["That did not go through (" + (err && err.message ? err.message : "network error") + "). You can ",
        mailLink(d, "send it from your mail app"), " instead, or post it in the ",
        h("a", { href: links.ideas || "#", target: "_blank", rel: "noopener", text: "ideas thread" }), "."]);
    }).then(function () { sendBtn.disabled = false; });
  }

  function buildDrawer() {
    scrim = h("div", { "class": "sw-scrim", onclick: close });
    var name = h("input", { id: "sw-name", name: "name", type: "text", required: "", maxlength: "120", autocomplete: "name", placeholder: "Your name" });
    var email = h("input", { id: "sw-email", name: "email", type: "email", required: "", maxlength: "200", autocomplete: "email", placeholder: "you@example.com" });
    var topic = h("select", { id: "sw-topic", name: "topic" });
    [["idea", "An idea or suggestion"], ["question", "A question"], ["collaboration", "Collaboration or a talk"],
     ["bug", "Something is wrong"], ["other", "Something else"]].forEach(function (o) {
      topic.appendChild(h("option", { value: o[0], text: o[1] }));
    });
    var msg = h("textarea", { id: "sw-message", name: "message", required: "", maxlength: "4000", minlength: "10",
      placeholder: "What is on your mind? Context helps: which page, which decision, what you expected." });
    var hp = h("div", { "class": "sw-hp", "aria-hidden": "true" }, [
      h("label", { "for": "sw-website", text: "Leave this field empty" }),
      h("input", { id: "sw-website", name: "website", type: "text", tabindex: "-1", autocomplete: "off" })]);
    sendBtn = h("button", { "class": "sw-send", type: "submit", text: "Send" });
    status = h("div", { "class": "sw-status", role: "status", "aria-live": "polite" });
    var consent = contact.endpoint
      ? "Your message is e-mailed to " + author + " and stored privately so it cannot get lost. It is never published or shared."
      : "Sending opens your own mail app with the message ready to go; nothing leaves this page otherwise.";
    var alt = h("div", { "class": "sw-alt" }, [
      h("span", { text: "Or:" }),
      h("a", { href: links.ideas || "#", target: "_blank", rel: "noopener", text: "post in the ideas thread" }),
      h("a", { href: "#", text: "use your mail app", onclick: function (ev) { ev.preventDefault(); location.href = mailtoHref(collect()); } })
    ]);
    form = h("form", { onsubmit: submit }, [
      field("Name", name), field("E-mail, so I can reply", email), field("Topic", topic), field("Message", msg), hp,
      h("p", { "class": "sw-consent", text: consent }), sendBtn, status, alt]);
    drawer = h("aside", { "class": "sw-drawer", id: "sw-contact", role: "dialog", "aria-modal": "true",
      "aria-labelledby": "sw-drawer-title", "aria-hidden": "true" }, [
      h("header", {}, [
        h("div", {}, [h("h2", { id: "sw-drawer-title", text: "Write to " + author }),
          h("p", { text: "Ideas, corrections, questions, collaborations. Short is fine." })]),
        h("button", { "class": "sw-x", type: "button", "aria-label": "Close", text: "×", onclick: close })]),
      form]);
    document.body.appendChild(scrim);
    document.body.appendChild(drawer);
  }

  function onKey(e) { if (e.key === "Escape") close(); }
  function open() {
    opener = document.activeElement;
    scrim.classList.add("on"); drawer.classList.add("on"); drawer.setAttribute("aria-hidden", "false");
    document.addEventListener("keydown", onKey);
    setTimeout(function () { var first = form.elements.name; if (first) first.focus(); }, 80);
  }
  function close() {
    scrim.classList.remove("on"); drawer.classList.remove("on"); drawer.setAttribute("aria-hidden", "true");
    document.removeEventListener("keydown", onKey);
    if (opener && opener.focus) opener.focus();
  }

  function build() {
    if (document.getElementById("sw-about")) return;
    document.body.appendChild(footer());
    buildDrawer();
    var pill = h("button", { "class": "sw-pill", type: "button", "aria-controls": "sw-contact", onclick: open }, [
      h("span", { "class": "sw-dot" }), "Built by " + author, h("small", { text: "· Ideas & contact" })]);
    document.body.appendChild(pill);
    Array.prototype.forEach.call(document.querySelectorAll("[data-sw-open]"), function (b) { b.addEventListener("click", open); });
    if (/[?#]contact\b/.test(location.href)) open();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build); else build();
})();
