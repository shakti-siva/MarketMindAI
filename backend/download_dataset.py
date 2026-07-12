import os
import shutil
import kagglehub

src = kagglehub.dataset_download(
    "nadyinky/sephora-products-and-skincare-reviews"
)

dst = r"D:\Projects\MarketMindAI\backend\data"
os.makedirs(dst, exist_ok=True)

for file_name in os.listdir(src):
    source_file = os.path.join(src, file_name)
    destination_file = os.path.join(dst, file_name)

    if os.path.isfile(source_file):
        shutil.copy(source_file, destination_file)

print("Dataset downloaded from:", src)
print("Dataset copied to:", dst)

print("\nFiles copied:")
for file_name in os.listdir(dst):
    print("-", file_name)