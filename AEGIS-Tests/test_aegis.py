# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import os
import sys
import time
import json
import unittest

# Add AEGIS paths to sys.path so we can import the modules
aegis_root = r'C:\Users\ROG G532 LV\.gemini\config\skills\aegis'
sys.path.append(os.path.join(aegis_root, 'AEGIS-Compiler'))
sys.path.append(os.path.join(aegis_root, 'AEGIS-Runtime'))
import importlib.util

# Load build.py dynamically to avoid naming conflict with stdlib 'build'
spec = importlib.util.spec_from_file_location("aegis_build", os.path.join(aegis_root, 'AEGIS-Compiler', 'build.py'))
aegis_build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aegis_build)

import kernel_runner

class TestAegisArchitecture(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n[TEST] Initializing AEGIS Test Environment...")
        cls.aegis_root = aegis_root
        
    def test_1_knowledge_compiler(self):
        print("\n[TEST] Testing Knowledge Compiler (build.py)...")
        start_time = time.time()
        
        # Run the compiler
        aegis_build.build_cognitive_pipeline()
        
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        # Verify that the 3 output graphs exist
        self.assertTrue(os.path.exists(os.path.join(self.aegis_root, 'runtime_image.json')))
        self.assertTrue(os.path.exists(os.path.join(self.aegis_root, 'instruction_graph.json')))
        self.assertTrue(os.path.exists(os.path.join(self.aegis_root, 'execution_graph.json')))
        
        # Validate JSON integrity
        with open(os.path.join(self.aegis_root, 'runtime_image.json'), 'r') as f:
            data = json.load(f)
            self.assertEqual(data["kernel_version"], "v12.0.0-executable-kernel")
            self.assertEqual(len(data["capabilities"]), 4)
            
        print(f"       -> SUCCESS: Compiled 3 Cognitive Graphs in {elapsed_ms:.2f} ms")

    def test_2_kernel_runtime(self):
        print("\n[TEST] Testing Cognitive Kernel (kernel_runner.py)...")
        start_time = time.time()
        
        vm = kernel_runner.AegisVirtualMachine(self.aegis_root)
        vm.boot()
        
        # Verify ISA is loaded correctly
        self.assertEqual(len(vm.isa.get("sequence", [])), 9)
        self.assertEqual(vm.isa["sequence"][0]["name"], "OBSERVE")
        
        # Execute the event loop
        vm.execute_event_loop("UNIT TEST DIAGNOSTIC TASK")
        
        end_time = time.time()
        elapsed_sec = (end_time - start_time)
        print(f"       -> SUCCESS: Kernel executed 9-Tick Cognitive Pipeline in {elapsed_sec:.2f} seconds")

if __name__ == '__main__':
    unittest.main(verbosity=2)
