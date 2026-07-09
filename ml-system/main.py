import os
import subprocess
import sys

def run_script(path):
    print(f"\n>>> Running {path}...")
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"Error executing {path}", file=sys.stderr)
        sys.exit(result.returncode)

def main():
    print("=========================================")
    print("         ML System Pipeline Run          ")
    print("=========================================")
    
    # 1. Preprocessing
    run_script("src/preprocessing/clean_data.py")
    
    # 2. Feature Engineering
    run_script("src/features/build_features.py")
    
    # 3. Training
    run_script("src/training/train_model.py")
    
    # 4. Batch Prediction
    run_script("src/prediction/predict_batch.py")
    
    print("\nPipeline execution complete.")

if __name__ == "__main__":
    main()
