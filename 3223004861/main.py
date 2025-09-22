import sys
import jieba
import math
from collections import defaultdict

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"文件不存在: {file_path}")
    except Exception as e:
        raise Exception(f"读取文件出错: {str(e)}")

def write_result(file_path, similarity):
    """写入结果到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{similarity:.2f}")
    except Exception as e:
        raise Exception(f"写入文件出错: {str(e)}")

def tokenize(text):
    """对文本进行分词处理"""
    # 使用jieba进行中文分词
    words = jieba.cut(text)
    # 过滤掉空字符串
    return [word for word in words if word.strip()]

def calculate_similarity(original_text, plagiarized_text):
    """计算两篇文本的相似度"""
    # 分词
    original_words = tokenize(original_text)
    plagiarized_words = tokenize(plagiarized_text)
    
    # 如果两个文本都为空，相似度为1.0
    if not original_words and not plagiarized_words:
        return 1.0
    # 如果其中一个文本为空，相似度为0.0
    if not original_words or not plagiarized_words:
        return 0.0
    
    # 构建词袋，统计词频
    word_counts = defaultdict(int)
    for word in original_words:
        word_counts[word] += 1
    for word in plagiarized_words:
        word_counts[word] += 1  # 这里只是为了获取所有词的集合
    
    # 构建向量
    original_vector = []
    plagiarized_vector = []
    for word in word_counts:
        original_vector.append(original_words.count(word))
        plagiarized_vector.append(plagiarized_words.count(word))
    
    # 计算余弦相似度
    dot_product = sum(a * b for a, b in zip(original_vector, plagiarized_vector))
    norm_original = math.sqrt(sum(a **2 for a in original_vector))
    norm_plagiarized = math.sqrt(sum(b** 2 for b in plagiarized_vector))
    
    if norm_original == 0 or norm_plagiarized == 0:
        return 0.0
    
    return dot_product / (norm_original * norm_plagiarized)

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件路径] [抄袭版论文文件路径] [答案文件路径]")
        sys.exit(1)
    
    original_path = sys.argv[1]
    plagiarized_path = sys.argv[2]
    result_path = sys.argv[3]
    
    try:
        # 读取文件内容
        original_text = read_file(original_path)
        plagiarized_text = read_file(plagiarized_path)
        
        # 计算相似度
        similarity = calculate_similarity(original_text, plagiarized_text)
        
        # 写入结果
        write_result(result_path, similarity)
        
    except Exception as e:
        print(f"程序出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
