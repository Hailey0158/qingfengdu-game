from pathlib import Path
import json, re
root = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame")

print("=== JSON ===")
ok = 0
for p in sorted(root.rglob("*.json")):
    try: json.loads(p.read_text(encoding="utf-8")); ok += 1
    except Exception as e: print("ERR", p.relative_to(root), e)
print(f"All {ok} JSON valid")

bt = json.loads((root / "data/branch-tree-mvp.json").read_text(encoding="utf-8"))
dl = json.loads((root / "data/final-dialogue/mvp/liu_lushu_day1.json").read_text(encoding="utf-8"))
bt_nodes = set(bt.get("nodes", {}).keys())
dl_nodes = set(dl.get("nodes", {}).keys())

print("\n=== NODE_COVERAGE ===")
print(f"Branch tree nodes: {len(bt_nodes)}")
print(f"Dialogue nodes: {len(dl_nodes)}")
in_bt_not_dl = bt_nodes - dl_nodes
print(f"BT has no dialogue: {sorted(in_bt_not_dl) if in_bt_not_dl else 'NONE'}")

ctrl = (root / "scripts/mvp_ui_controller.gd").read_text(encoding="utf-8")
runner = (root / "scripts/mvp_scene_runner.gd").read_text(encoding="utf-8")

# Check initial scene
m = re.search(r'current_scene_id.*=.*"([^"]+)"', runner)
print(f"\nInitial scene: {m.group(1) if m else 'NOT_FOUND'}")

# Reachability from ch1_title
reachable = set()
stack = ["ch1_title"]
while stack:
    nid = stack.pop()
    if nid not in bt_nodes or nid in reachable: continue
    reachable.add(nid)
    for c in bt["nodes"][nid].get("choices", []):
        t = c.get("target_node", "")
        if t and t in bt_nodes: stack.append(t)
unreachable = bt_nodes - reachable
print(f"\n=== REACHABILITY ===")
print(f"Start=ch1_title, reachable={len(reachable)}/{len(bt_nodes)}")
print(f"Unreachable: {sorted(unreachable) if unreachable else 'NONE'}")

missing_targets = []
for nid, node in bt["nodes"].items():
    for c in node.get("choices", []):
        t = c.get("target_node", "")
        if t and t not in bt_nodes: missing_targets.append(f"{nid} -> {t}")
print(f"Missing targets: {missing_targets if missing_targets else 'NONE'}")

# Check chapter titles in dialogue
for ch in ["ch1_title", "ch2_title", "ch3_title"]:
    if ch in dl_nodes:
        print(f"\n{ch} dialogue: {dl['nodes'][ch]['text'][:60]}...")

# BG coverage
missing_bg = [n for n in bt_nodes if n not in ctrl]
print(f"\n=== BG_COVERAGE ===")
print(f"Missing: {missing_bg if missing_bg else 'NONE'}")

print("\n=== ALL_CHECKS_DONE ===")
