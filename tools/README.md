# HRM-MLX Dataset Tools

This directory contains tools for creating and managing test datasets for the HRM-MLX project.

## Available Tools

### 1. `prep_data.py` - Dataset Preparation Tool

Creates sample datasets for testing the hierarchical reasoning model.

**Usage:**
```bash
# Create a reasoning dataset (default)
python tools/prep_data.py --output data/processed/reasoning_data.json --num_samples 100

# Create different types of datasets
python tools/prep_data.py --type sudoku --num_samples 50 --output data/processed/sudoku_data.json
python tools/prep_data.py --type sequence --num_samples 75 --output data/processed/sequence_data.json
python tools/prep_data.py --type all --num_samples 90 --output data/processed/mixed_data.json

# Process existing dataset (as mentioned in README)
python tools/prep_data.py --input data/sample.json --output data/processed/sample_processed.json
```

**Dataset Types:**
- **reasoning**: Multi-hop arithmetic reasoning problems
- **sudoku**: Sudoku puzzles with solutions (81-element sequences)
- **sequence**: Pattern completion tasks (arithmetic, geometric, fibonacci)
- **all**: Mixed dataset with all types

### 2. `test_dataset.py` - Dataset Testing and Validation Tool

Validates and analyzes dataset files to ensure they're properly formatted.

**Usage:**
```bash
# Basic dataset inspection
python tools/test_dataset.py --input data/sample.json

# Run validation checks
python tools/test_dataset.py --input data/processed/sudoku_test.json --validate

# Show more sample data
python tools/test_dataset.py --input data/processed/reasoning_test.json --show_samples 5
```

## Dataset Formats

### Reasoning Dataset Format
```json
{
  "id": "reasoning_0001",
  "input": "Given x = 5, and y = x + 3, what is y * 2?",
  "steps": [
    "Step 1: x = 5",
    "Step 2: y = x + 3 = 5 + 3 = 8", 
    "Step 3: y * 2 = 8 * 2 = 16"
  ],
  "target": 16,
  "difficulty": "easy"
}
```

### Sudoku Dataset Format
```json
{
  "id": "sudoku_0001",
  "puzzle": [5,3,0,0,7,0,0,0,0, ...],  // 81 integers, 0 for blanks
  "solution": [5,3,4,6,7,8,9,1,2, ...], // 81 integers, 1-9 for solution
  "difficulty": "easy",
  "blanks": 51
}
```

### Sequence Dataset Format
```json
{
  "id": "sequence_0001",
  "sequence": [1, 3, 5, 7, 9],
  "target": 11,
  "type": "arithmetic",
  "difficulty": "easy"
}
```

## Quick Start

1. **Create your first test dataset:**
   ```bash
   python tools/prep_data.py --type reasoning --num_samples 20 --output data/my_test.json
   ```

2. **Validate the dataset:**
   ```bash
   python tools/test_dataset.py --input data/my_test.json --validate
   ```

3. **Use with HRM-MLX training (when available):**
   ```bash
   python -m hrmlx.run --config configs/quick_test.yaml --data data/my_test.json --output results/
   ```

## Tips

- Start with small datasets (10-50 samples) for initial testing
- Use `--validate` flag to ensure data quality
- Mix different dataset types for comprehensive testing
- Check the `data/sample.json` file for format examples
- Sudoku datasets work well with the existing HRM training scripts

## Extending the Tools

To add new dataset types:

1. Create a new function like `create_your_type_dataset()` in `prep_data.py`
2. Add the new type to the `choices` in the argument parser
3. Add validation logic in `test_dataset.py`
4. Update this README with the new format

## Example Workflow

```bash
# 1. Create test datasets
python tools/prep_data.py --type all --num_samples 30 --output data/test_mixed.json

# 2. Validate the data
python tools/test_dataset.py --input data/test_mixed.json --validate --show_samples 5

# 3. Train with the data (using existing scripts)
./train_small.sh  # Uses internal Sudoku data

# 4. Create custom reasoning data
python tools/prep_data.py --type reasoning --num_samples 100 --output data/custom_reasoning.json
```
