import random

# 示例字典map_attr_type
map_attr_type = {
    "attribute1": "temporal",
    "attribute2": "categorical",
    "attribute3": "temporal",
    "attribute4": "numerical",
}

# 从"temporal"类别的属性中随机选择一个属性名称
temporal_attributes = [attr for attr, attr_type in map_attr_type.items() if attr_type == "temporal"]
print(temporal_attributes)
if temporal_attributes:
    random_temporal_attr = random.choice(temporal_attributes)
    print(f"随机选择的'temporal'属性名称是: {random_temporal_attr}")
else:
    print("没有找到'temporal'属性")