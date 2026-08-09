from pathlib import Path
import json, re

root = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame")

print("JSON_VALIDATION")
for p in sorted(root.rglob("*.json")):
    try:
        json.loads(p.read_text(encoding="utf-8"))
        print("OK", p.relative_to(root))
    except Exception as e:
        print("ERR", p.relative_to(root), e)

print("\nBRANCH_REACHABILITY")
bt = json.loads((root / "data/branch-tree-mvp.json").read_text(encoding="utf-8"))
nodes = bt["nodes"]
reachable = set()
stack = ["scene_001a_rain_lantern"]
while stack:
    nid = stack.pop()
    if nid in reachable or nid not in nodes:
        continue
    reachable.add(nid)
    for c in nodes[nid].get("choices", []):
        t = c.get("target_node", "")
        if t:
            stack.append(t)
all_nodes = set(nodes.keys())
unreachable = all_nodes - reachable
print("start=scene_001a_rain_lantern reachable=" + str(len(reachable)) + " total=" + str(len(all_nodes)))
print("unreachable", unreachable if unreachable else "NONE")
missing_targets = []
for nid, node in nodes.items():
    for c in node.get("choices", []):
        t = c.get("target_node", "")
        if t and t not in nodes:
            missing_targets.append(nid + "->" + t)
print("missing_targets", missing_targets if missing_targets else "NONE")

print("\nSCENE_REFERENCES")
scene_files = [
    root / "scenes/main.tscn",
    root / "scenes/character_sprite.tscn",
    root / "scripts/mvp_ui_controller.gd",
    root / "scripts/mvp_scene_runner.gd",
]
missing_refs = []
for p in scene_files:
    text = p.read_text(encoding="utf-8")
    for ref in re.findall(r'res://[^"\s)]+', text):
        q = root / ref[6:]
        if not q.exists():
            missing_refs.append((p.name, ref))
print("missing_refs", missing_refs if missing_refs else "NONE")

print("\nNODE_CHECK")
main_text = (root / "scenes/main.tscn").read_text(encoding="utf-8")
ctrl_text = (root / "scripts/mvp_ui_controller.gd").read_text(encoding="utf-8")
for node in ["InnkeeperPortrait", "LiuPortrait", "LiPortrait", "GuiPortrait", "BackgroundLayer"]:
    in_scene = ('name="' + node + '"') in main_text
    in_ctrl = node in ctrl_text
    print(node + ": scene=" + str(in_scene) + " controller=" + str(in_ctrl))

print("\nINITIAL_SCENE")
runner_text = (root / "scripts/mvp_scene_runner.gd").read_text(encoding="utf-8")
m = re.search(r'current_scene_id.*=.*"([^"]+)"', runner_text)
print("initial_scene_id=", m.group(1) if m else "NOT_FOUND")

print("\nDIALOGUE_NODES")
dl = json.loads((root / "data/final-dialogue/mvp/liu_lushu_day1.json").read_text(encoding="utf-8"))
for nid in ["scene_001a_rain_lantern", "scene_001b_innkeeper", "scene_001c_choices"]:
    entry = dl["nodes"].get(nid, {})
    text_preview = entry.get("text", "")[:80]
    print(nid + ": speaker=" + entry.get("speaker", "?") + " text=" + text_preview + "...")

print("\nALL_CHECKS_DONE")
