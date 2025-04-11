import re


def process_csv_content(csv_str):
    lines = csv_str.strip().split("\n")
    processed_lines = []
    pattern = re.compile(r'^\d{16}')

    # 初始化一个空字符串用于收集合并的行
    current_line = ""

    for line in lines:
        # 检查每行是否以16位数字开头
        if pattern.match(line):
            # 如果当前行有内容，说明它是上一个以16位数字开头的行的延续
            if current_line:
                # 将当前行加入到processed_lines中
                processed_lines.append(current_line)
                # 重置current_line为新的以16位数字开头的行
                current_line = line
            else:
                # 如果current_line为空，说明这是第一个以16位数字开头的行
                current_line = line
        else:
            # 如果当前行不以16位数字开头，则将其内容添加到current_line中
            current_line += " " + line.strip()

    # 确保最后一行也被添加到processed_lines中
    if current_line:
        processed_lines.append(current_line)

    return "\n".join(processed_lines)


# 读取CSV文件
with open(r'..\结果\weibo-x.csv', 'r', encoding='utf-8') as file:
    content = file.read()

# 处理CSV内容
processed_content = process_csv_content(content)

# 将处理后的内容写回到一个新的CSV文件
with open(r'..\结果\processed_weibo-x.csv', 'w', encoding='utf-8') as file:
    file.write(processed_content)
