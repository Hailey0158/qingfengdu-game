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

print("\nSCENE_REFERENCES")
scene_files = [
    root / "scenes/main.tscn",
    root / "scenes/character_sprite.tscn",
    root / "scenes/dialogue_box.tscn",
    root / "scripts/mvp_ui_controller.gd",
    root / "scripts/mvp_scene_runner.gd",
]
missing = []
for p in scene_files:
    text = p.read_text(encoding="utf-8")
    for ref in re.findall(r'res://[^"\s)]+', text):
        if not (root / ref[6:]).exists():
            missing.append((p.name, ref))
print("MISSING_REFS", missing if missing else "NONE")

print("\nLAYOUT_VERIFICATION")
main = (root / "scenes/main.tscn").read_text(encoding="utf-8")
dialogue = (root / "scenes/dialogue_box.tscn").read_text(encoding="utf-8")
checks = [
    ("InnkeeperPortrait right side", 'offset_left = 860.0' in main and 'name="InnkeeperPortrait"' in main),
    ("Portraits shortened", 'offset_bottom = 440.0' in main),
    ("DialogueBox enlarged", 'offset_top = 370.0' in main and 'offset_bottom = 680.0' in main),
    ("ChoicePanel repositioned", 'offset_top = 190.0' in main and 'offset_bottom = 360.0' in main),
    ("DialogueBox min height 310", "Vector2(0, 310)" in dialogue),
    ("DialogueText min height 240", "Vector2(0, 240)" in dialogue),
]
for name, ok in checks:
    print(("OK" if ok else "FAIL"), name)

ctrl = (root / "scripts/mvp_ui_controller.gd").read_text(encoding="utf-8")
assert "bg_three_characters_scene.png" in ctrl
assert "scene_010_meet" in ctrl
assert 'show_liu: bool = node_id == "scene_020_liu_day1" or node_id == "scene_021_liu_day1_close"' in ctrl
assert "show_li: bool = false" in ctrl
assert "show_gui: bool = false" in ctrl
print("CHARACTER_VISIBILITY_OK")

three_char_bg = root / "assets/placeholder_sprites/bg_three_characters_scene.png"
print("THREE_CHAR_BG", three_char_bg.exists(), three_char_bg.stat().st_size if three_char_bg.exists() else "MISSING")

orphans = [str(p.relative_to(root)) for p in root.rglob("*.import") if not p.with_suffix("").exists()]
print("IMPORT_ORPHANS", orphans if orphans else "NONE")
print("\nALL_CHECKS_DONE")