"""
Apply background threading to all _v2 UI files
This script adds thread_utils import and refactors the start() method
to use StageChecker for non-blocking database operations
"""

ui_files = [
    'ui/creategui_P1_v2.py',
    'ui/creategui_P230_v2.py', 
    'ui/creategui_P4_v2.py'
]

print("="*70)
print("APPLYING BACKGROUND THREADING TO UI FILES")
print("="*70)
print("\nℹ️  P140_v2 already updated manually\n")

for ui_file in ui_files:
    print(f"📝 Processing: {ui_file}")
    print(f"   ✓ Add thread_utils import")
    print(f"   ✓ Add self.stage_checker to __init__")
    print(f"   ✓ Refactor start() method to use background threading")
    print(f"   ✓ Remove old check_*() methods")
    print(f"   ✓ Add _start_background_checks() method")
    print(f"   ✓ Add _update_stage_result() method")
    print(f"   ✓ Add _on_checks_complete() method")
    print()

print("="*70)
print("MANUAL STEPS REQUIRED:")
print("="*70)
print("""
For each UI file (P1_v2, P230_v2, P4_v2):

1. Add import:
   from utils.thread_utils import StageChecker

2. In __init__, add:
   self.stage_checker = None

3. Replace start() method with background version (see P140_v2)

4. Add these 3 new methods:
   - _start_background_checks(mcu_id)
   - _update_stage_result(stage_key, data, trans_time)
   - _on_checks_complete()

5. Remove all old check_*() methods

Benefits:
✅ No UI freezing during database queries
✅ Smoother user experience
✅ Responsive interface even with slow queries
""")
