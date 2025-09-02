#!/usr/bin/env python3
"""
Simple test runner for HRM-MLX datasets
Demonstrates how to load and use test datasets
"""

import json
import argparse
import os
from typing import List, Dict, Any

def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """Load dataset from JSON file"""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print(f"📊 Loaded {len(data)} samples from {file_path}")
    return data

def analyze_dataset(data: List[Dict[str, Any]]):
    """Analyze dataset structure and content"""
    
    print("\n🔍 Dataset Analysis:")
    print(f"  Total samples: {len(data)}")
    
    if not data:
        return
    
    # Check data types
    sample_keys = set(data[0].keys())
    print(f"  Sample keys: {sample_keys}")
    
    # Check for different data types
    data_types = set()
    for sample in data:
        if 'puzzle' in sample:
            data_types.add('sudoku')
        elif 'sequence' in sample:
            data_types.add('sequence')
        elif 'steps' in sample:
            data_types.add('reasoning')
        else:
            data_types.add('unknown')
    
    print(f"  Data types: {data_types}")
    
    # Check difficulties if available
    if 'difficulty' in data[0]:
        difficulties = {}
        for sample in data:
            diff = sample.get('difficulty', 'unknown')
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        print(f"  Difficulty distribution:")
        for diff, count in difficulties.items():
            print(f"    {diff}: {count} samples")

def validate_reasoning_sample(sample: Dict[str, Any]) -> bool:
    """Validate a reasoning sample"""
    
    required_keys = ['id', 'input', 'target']
    for key in required_keys:
        if key not in sample:
            print(f"❌ Missing key '{key}' in sample {sample.get('id', 'unknown')}")
            return False
    
    return True

def validate_sudoku_sample(sample: Dict[str, Any]) -> bool:
    """Validate a Sudoku sample"""
    
    required_keys = ['id', 'puzzle', 'solution']
    for key in required_keys:
        if key not in sample:
            print(f"❌ Missing key '{key}' in sample {sample.get('id', 'unknown')}")
            return False
    
    # Check puzzle and solution lengths
    puzzle = sample['puzzle']
    solution = sample['solution']
    
    if len(puzzle) != 81:
        print(f"❌ Invalid puzzle length: {len(puzzle)} (expected 81)")
        return False
    
    if len(solution) != 81:
        print(f"❌ Invalid solution length: {len(solution)} (expected 81)")
        return False
    
    # Check value ranges
    for val in puzzle:
        if not (0 <= val <= 9):
            print(f"❌ Invalid puzzle value: {val} (expected 0-9)")
            return False
    
    for val in solution:
        if not (1 <= val <= 9):
            print(f"❌ Invalid solution value: {val} (expected 1-9)")
            return False
    
    return True

def validate_dataset(data: List[Dict[str, Any]]):
    """Validate dataset samples"""
    
    print("\n✅ Validating dataset...")
    
    valid_count = 0
    
    for i, sample in enumerate(data):
        is_valid = True
        
        # Determine sample type and validate accordingly
        if 'puzzle' in sample:
            is_valid = validate_sudoku_sample(sample)
        elif 'steps' in sample:
            is_valid = validate_reasoning_sample(sample)
        elif 'sequence' in sample:
            # Basic validation for sequence samples
            required_keys = ['id', 'sequence', 'target']
            for key in required_keys:
                if key not in sample:
                    print(f"❌ Missing key '{key}' in sample {sample.get('id', 'unknown')}")
                    is_valid = False
        
        if is_valid:
            valid_count += 1
        else:
            print(f"❌ Sample {i} is invalid")
    
    print(f"✅ {valid_count}/{len(data)} samples are valid")

def show_samples(data: List[Dict[str, Any]], num_samples: int = 3):
    """Show sample data"""
    
    print(f"\n📋 Showing first {min(num_samples, len(data))} samples:")
    
    for i in range(min(num_samples, len(data))):
        print(f"\n--- Sample {i+1} ---")
        sample = data[i]
        
        # Pretty print based on sample type
        if 'puzzle' in sample:
            print(f"ID: {sample['id']}")
            print(f"Type: Sudoku")
            print(f"Difficulty: {sample.get('difficulty', 'unknown')}")
            print(f"Blanks: {sample.get('blanks', 'unknown')}")
            print("Puzzle (first 9 cells):", sample['puzzle'][:9])
            
        elif 'steps' in sample:
            print(f"ID: {sample['id']}")
            print(f"Type: Reasoning")
            print(f"Input: {sample['input']}")
            print(f"Target: {sample['target']}")
            print(f"Steps: {len(sample.get('steps', []))}")
            
        elif 'sequence' in sample:
            print(f"ID: {sample['id']}")
            print(f"Type: Sequence")
            print(f"Sequence: {sample['sequence']}")
            print(f"Target: {sample['target']}")
            print(f"Sequence type: {sample.get('type', 'unknown')}")

def main():
    parser = argparse.ArgumentParser(description="Test dataset loading and validation")
    parser.add_argument("--input", type=str, default="data/sample.json", 
                       help="Input dataset file")
    parser.add_argument("--validate", action="store_true", 
                       help="Run validation checks")
    parser.add_argument("--show_samples", type=int, default=3,
                       help="Number of samples to display")
    
    args = parser.parse_args()
    
    print("🧪 HRM-MLX Dataset Tester")
    print("=" * 40)
    
    try:
        # Load dataset
        data = load_dataset(args.input)
        
        # Analyze dataset
        analyze_dataset(data)
        
        # Validate if requested
        if args.validate:
            validate_dataset(data)
        
        # Show samples
        if args.show_samples > 0:
            show_samples(data, args.show_samples)
        
        print("\n🎉 Dataset test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
