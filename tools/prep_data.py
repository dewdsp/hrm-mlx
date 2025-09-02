#!/usr/bin/env python3
"""
Dataset preparation tool for HRM-MLX
Creates sample datasets for testing the hierarchical reasoning model
"""

import argparse
import json
import random
import numpy as np
from typing import List, Dict, Any
import os

def create_simple_reasoning_dataset(num_samples: int = 100) -> List[Dict[str, Any]]:
    """
    Create a simple multi-hop reasoning dataset
    Each sample requires the model to perform multiple reasoning steps
    """
    
    samples = []
    
    for i in range(num_samples):
        # Create a simple arithmetic reasoning chain
        # Example: "If x = 3 and y = x + 2, what is y * 2?"
        
        x = random.randint(1, 10)
        y = x + random.randint(1, 5)
        z = y * random.randint(2, 4)
        
        # Multi-step reasoning problem
        problem = f"Given x = {x}, and y = x + {y - x}, what is y * {z // y}?"
        
        # Break down into steps for hierarchical reasoning
        steps = [
            f"Step 1: x = {x}",
            f"Step 2: y = x + {y - x} = {x} + {y - x} = {y}",
            f"Step 3: y * {z // y} = {y} * {z // y} = {z}"
        ]
        
        sample = {
            "id": f"reasoning_{i:04d}",
            "input": problem,
            "steps": steps,
            "target": z,
            "difficulty": "easy" if z < 50 else "medium" if z < 100 else "hard"
        }
        
        samples.append(sample)
    
    return samples

def create_sudoku_test_dataset(num_samples: int = 50) -> List[Dict[str, Any]]:
    """
    Create a small Sudoku test dataset
    Each puzzle is represented as a sequence of 81 numbers (0 for blanks, 1-9 for digits)
    """
    
    # Simple pre-made Sudoku puzzles for testing
    # These are valid but simple puzzles
    sample_puzzles = [
        # Easy puzzle 1
        "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
        # Easy puzzle 2  
        "200080300060070084030500209000105408000000000402706000301007040720040060004010003",
        # Medium puzzle
        "000000907000420180000705026100904000050000040000507009920108000034059000507000000"
    ]
    
    sample_solutions = [
        "534678912672195348198342567859761423426853791713924856961537284287419635345286179",
        "245981376169273584837564219976125438513498627482736951351827945728349165694615832", 
        "218643957967428185543715826176924538852316743394587269925178364634259871587361492"
    ]
    
    samples = []
    
    for i in range(num_samples):
        # Cycle through the sample puzzles
        puzzle_idx = i % len(sample_puzzles)
        puzzle_str = sample_puzzles[puzzle_idx]
        solution_str = sample_solutions[puzzle_idx]
        
        # Convert to lists of integers
        puzzle = [int(c) for c in puzzle_str]
        solution = [int(c) for c in solution_str]
        
        sample = {
            "id": f"sudoku_{i:04d}",
            "puzzle": puzzle,
            "solution": solution,
            "difficulty": random.choice(["easy", "medium"]),
            "blanks": puzzle.count(0)
        }
        
        samples.append(sample)
    
    return samples

def create_sequence_completion_dataset(num_samples: int = 100) -> List[Dict[str, Any]]:
    """
    Create a sequence completion dataset for testing adaptive computation
    """
    
    samples = []
    
    for i in range(num_samples):
        # Create different types of sequences
        seq_type = random.choice(["arithmetic", "geometric", "fibonacci", "pattern"])
        
        if seq_type == "arithmetic":
            start = random.randint(1, 10)
            diff = random.randint(1, 5)
            length = random.randint(5, 8)
            sequence = [start + i * diff for i in range(length)]
            next_val = start + length * diff
            
        elif seq_type == "geometric":
            start = random.randint(1, 5)
            ratio = random.randint(2, 3)
            length = random.randint(4, 6)
            sequence = [start * (ratio ** i) for i in range(length)]
            next_val = start * (ratio ** length)
            
        elif seq_type == "fibonacci":
            sequence = [1, 1]
            length = random.randint(6, 8)
            for j in range(2, length):
                sequence.append(sequence[j-1] + sequence[j-2])
            next_val = sequence[-1] + sequence[-2]
            
        else:  # pattern
            base = random.randint(1, 5)
            sequence = [base, base*2, base, base*2, base, base*2]
            next_val = base
        
        sample = {
            "id": f"sequence_{i:04d}",
            "sequence": sequence,
            "target": next_val,
            "type": seq_type,
            "difficulty": "easy" if len(sequence) <= 5 else "medium"
        }
        
        samples.append(sample)
    
    return samples

def save_dataset(data: List[Dict[str, Any]], output_path: str):
    """Save dataset to JSON file"""
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(data)} samples to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Create test datasets for HRM-MLX")
    parser.add_argument("--input", type=str, 
                       help="Input dataset file (optional, for processing existing data)")
    parser.add_argument("--output", type=str, default="data/processed/sample_processed.json", 
                       help="Output path for the dataset")
    parser.add_argument("--type", type=str, choices=["reasoning", "sudoku", "sequence", "all"], 
                       default="reasoning", help="Type of dataset to create")
    parser.add_argument("--num_samples", type=int, default=100, 
                       help="Number of samples to generate")
    
    args = parser.parse_args()
    
    print(f"🔧 Creating {args.type} dataset with {args.num_samples} samples...")
    
    # If input file is provided, load and process it
    if args.input and os.path.exists(args.input):
        print(f"📂 Loading existing data from {args.input}")
        with open(args.input, 'r') as f:
            existing_data = json.load(f)
        
        # Process existing data (for now, just copy it)
        data = existing_data
        print(f"📋 Loaded {len(data)} existing samples")
    else:
        # Generate new data
        if args.type == "reasoning":
            data = create_simple_reasoning_dataset(args.num_samples)
        elif args.type == "sudoku":
            data = create_sudoku_test_dataset(args.num_samples)
        elif args.type == "sequence":
            data = create_sequence_completion_dataset(args.num_samples)
        elif args.type == "all":
            # Create a mixed dataset
            reasoning_data = create_simple_reasoning_dataset(args.num_samples // 3)
            sudoku_data = create_sudoku_test_dataset(args.num_samples // 3)
            sequence_data = create_sequence_completion_dataset(args.num_samples // 3)
            data = reasoning_data + sudoku_data + sequence_data
            random.shuffle(data)
    
    save_dataset(data, args.output)
    
    # Print sample
    print(f"\n📋 Sample data:")
    print(json.dumps(data[0], indent=2))
    
    print(f"\n📊 Dataset summary:")
    print(f"  Total samples: {len(data)}")
    if 'difficulty' in data[0]:
        difficulties = [sample['difficulty'] for sample in data]
        for diff in set(difficulties):
            print(f"  {diff.capitalize()}: {difficulties.count(diff)} samples")

if __name__ == "__main__":
    main()
