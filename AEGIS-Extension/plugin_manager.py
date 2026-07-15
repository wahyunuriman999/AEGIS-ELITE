"""
AEGIS-Extension: Marketplace plugin manager stub.
"""

class PluginManager:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def list_available(self):
        print("AEGIS Extension Marketplace: No plugins available in stub mode.")

    def install(self, pack_id: str):
        print(f"Installing pack: {pack_id} (stubbed)")

    def remove(self, pack_id: str):
        print(f"Removing pack: {pack_id} (stubbed)")

    def update(self, pack_id: str):
        print(f"Updating pack: {pack_id} (stubbed)")


if __name__ == "__main__":
    pm = PluginManager('.')
    pm.list_available()
