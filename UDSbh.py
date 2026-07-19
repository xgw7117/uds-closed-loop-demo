#import udsoncan
#from udsoncan import services
import random

# ----- 1. 0x27 安全访问：种子 -> 密钥 -----
seed = random.randint(0, 0xFFFFFFFF)
# 算法：种子 XOR 0xA5A5A5A5，取后6位
temp = (seed ^ 0xA5A5A5A5) & 0xFFFFFFFF
key = temp % 1000000  # 取后6位作为密钥
print(f"Step1 0x27: seed={hex(seed)} -> key={key}")

# 2. 0x22 读取数据（依赖 key）
did = key % 0xFFFF
read_data = (key * 0x9E37 + 0x7A1B) & 0xFFFFFFFF  # 关键：依赖 key
print(f"Step2 0x22: DID=0x{did:04X} -> read_data=0x{read_data:08X}")

# 3. 0x2E 写入数据（依赖 read_data）
write_val = read_data & 0xFFFFFF
checksum = ((write_val & 0xFF) + ((write_val>>8)&0xFF) + ((write_val>>16)&0xFF)) % 1000000
print(f"Step3 0x2E: write_data=0x{write_val:06X} -> checksum={checksum}")

# 4. 0x19 读取DTC（依赖 checksum）
mask = checksum
dtc_count = (mask * 17 + 3) % 100
final_output = (dtc_count * 83 + 17) % 1000

print(f"Step4 0x19: mask=0x{mask:04X} -> dtc_count={dtc_count} -> final={final_output}")