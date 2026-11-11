import os
import subprocess

def test_analytics_event_emitted(run_case):
    device = os.getenv("ARTEMIS_DEVICE", "emulator-5554")
    subprocess.run(["adb", "-s", device, "shell", "setprop", "log.tag.FA", "VERBOSE"], check=True)
    subprocess.run(["adb", "-s", device, "shell", "setprop", "log.tag.FA-SVC", "VERBOSE"], check=True)
    subprocess.run(["adb", "-s", device, "shell", "setprop", "debug.firebase.analytics.app", "com.eventhub.app"], check=True)
    subprocess.run(["adb", "-s", device, "shell", "am", "force-stop", "com.eventhub.app"], check=True)
    subprocess.run(["adb", "-s", device, "logcat", "-c"], check=True)
    subprocess.run(["adb", "-s", device, "shell", "am", "start", "-n", "com.eventhub.app/.MainActivity"], check=True)
    try:
        run_case("TC18", "Sign in with {account}. Open Account > Firebase tools and Fetch new config. Wait for feedback.", "L3-01", "Giới hạn gợi ý")
        log = subprocess.run(["adb", "-s", device, "logcat", "-d", "-s", "FA", "FA-SVC"], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        assert "remote_config_fetch" in log, "Analytics event not observed in native debug logs; console DebugView screenshot is still required"
    finally:
        subprocess.run(["adb", "-s", device, "shell", "setprop", "debug.firebase.analytics.app", ".none."], check=True)
        subprocess.run(["adb", "-s", device, "shell", "setprop", "log.tag.FA", "INFO"], check=True)
        subprocess.run(["adb", "-s", device, "shell", "setprop", "log.tag.FA-SVC", "INFO"], check=True)



