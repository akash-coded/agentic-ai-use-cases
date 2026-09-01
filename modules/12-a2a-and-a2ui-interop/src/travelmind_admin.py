
import json
import streamlit as st

st.set_page_config(page_title="TravelMind A2UI Admin", layout="wide")
st.title("TravelMind A2UI Admin")

audit = json.load(open("audit_log.json"))
surfaces = json.load(open("captured_surfaces.json"))

CONTAINER = {"Column", "Row"}


def resolve(b):
    if not isinstance(b, dict):
        return str(b)
    return b.get("literalString", b.get("path", ""))


def render_lines(messages):
    comps, root = {}, None
    for m in messages:
        if "surfaceUpdate" in m:
            for c in m["surfaceUpdate"]["components"]:
                comps[c["id"]] = c["component"]
        elif "beginRendering" in m:
            root = m["beginRendering"]["root"]
    out = []

    def walk(cid, d):
        node = comps.get(cid)
        if not node:
            return
        t = list(node)[0]
        body = node[t]
        pad = "  " * d
        if t == "Text":
            out.append(pad + resolve(body.get("text", {})))
        elif t == "Button":
            child = body.get("child")
            lbl = resolve(comps.get(child, {}).get("Text", {}).get("text", {})) if child in comps else child
            out.append(pad + f"[ {lbl} ]  -> {body['action']['name']}")
        elif t == "MetricCard":
            out.append(pad + f"+-- {resolve(body['label'])}: {resolve(body['value'])} --+")
        elif t in CONTAINER:
            out.append(pad + t + ":")
            for ch in body.get("children", {}).get("explicitList", []):
                walk(ch, d + 1)

    if root:
        walk(root, 0)
    return "\n".join(out)


c1, c2, c3, c4 = st.columns(4)
c1.metric("Surfaces emitted", sum(1 for a in audit if a["kind"] == "ui_emitted"))
c2.metric("User actions", sum(1 for a in audit if a["kind"] == "user_action"))
c3.metric("Authorizations", sum(1 for a in audit if a["kind"] == "authorization"))
c4.metric("Bookings", sum(1 for a in audit if a["kind"] == "tool_executed"))

st.subheader("Event timeline")
st.dataframe(audit, use_container_width=True)

st.subheader("Surface inspector")
labels = [f"{i}: {s['kind']} ({s['surfaceId']})" for i, s in enumerate(surfaces)]
if labels:
    pick = st.selectbox("Captured surface", range(len(labels)), format_func=lambda i: labels[i])
    left, right = st.columns(2)
    with left:
        st.caption("What the user saw")
        st.code(render_lines(surfaces[pick]["messages"]) or "(empty)")
    with right:
        st.caption("Raw A2UI payload")
        st.json(surfaces[pick]["messages"])
else:
    st.info("No surfaces captured yet.")
