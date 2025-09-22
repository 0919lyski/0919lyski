import unittest
import os
import tempfile
from main import calculate_similarity, read_file, write_result

class TestPaperChecker(unittest.TestCase):
    
    def test_identical_text(self):
        """测试完全相同的文本"""
        text1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        text2 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        self.assertAlmostEqual(calculate_similarity(text1, text2), 1.0, places=2)
    
    def test_similar_text(self):
        """测试示例中的相似文本"""
        original = "今天是星期天，天气晴，今天晚上我要去看电影。"
        plagiarized = "今天是周天，天气晴朗，我晚上要去看电影。"
        similarity = calculate_similarity(original, plagiarized)
        # 预期相似度应该在0.7左右
        self.assertTrue(0.6 <= similarity <= 0.8)
    
    def test_empty_texts(self):
        """测试两个空文本"""
        self.assertEqual(calculate_similarity("", ""), 1.0)
    
    def test_one_empty_text(self):
        """测试一个空文本和一个非空文本"""
        self.assertEqual(calculate_similarity("", "测试文本"), 0.0)
        self.assertEqual(calculate_similarity("测试文本", ""), 0.0)
    
    def test_completely_different(self):
        """测试完全不同的文本"""
        text1 = "这是第一段测试文本，包含一些独特的词语。"
        text2 = "完全不同的内容，没有任何重复的词汇在这里出现。"
        similarity = calculate_similarity(text1, text2)
        self.assertLess(similarity, 0.1)
    
    def test_partially_similar(self):
        """测试部分相似的文本"""
        text1 = "机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习。"
        text2 = "人工智能的分支之一是机器学习，它让计算机可以不用明确编程就能进行学习。"
        similarity = calculate_similarity(text1, text2)
        self.assertTrue(0.7 <= similarity <= 0.9)
    
    def test_read_file(self):
        """测试文件读取功能"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("测试文件内容")
            temp_name = f.name
        
        # 测试读取
        content = read_file(temp_name)
        self.assertEqual(content, "测试文件内容")
        
        # 清理临时文件
        os.unlink(temp_name)
    
    def test_write_file(self):
        """测试文件写入功能"""
        # 创建临时文件路径
        temp_name = tempfile.mktemp()
        
        # 测试写入
        write_result(temp_name, 0.75)
        
        # 验证内容
        with open(temp_name, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, "0.75")
        
        # 清理临时文件
        os.unlink(temp_name)
    
    def test_special_characters(self):
        """测试包含特殊字符的文本"""
        text1 = "文本中包含各种特殊字符：!@#$%^&*()_+{}|:\"<>?`-=[]\\;',./"
        text2 = "特殊字符测试：!@#$%^&*()_+{}|:\"<>?`-=[]\\;',./ 还有一些额外内容"
        similarity = calculate_similarity(text1, text2)
        self.assertTrue(0.5 <= similarity <= 0.7)
    
    def test_large_text(self):
        """测试长文本"""
        text1 = "重复" * 1000 + "独特内容"
        text2 = "重复" * 800 + "不同内容"
        similarity = calculate_similarity(text1, text2)
        self.assertTrue(0.8 <= similarity <= 0.95)

if __name__ == '__main__':
    unittest.main()
