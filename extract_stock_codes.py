#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从stock.jpg中提取第二列的股票代码，保存到stock.txt文件
"""

import os
import cv2
import pytesseract
from PIL import Image

class StockCodeExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
    
    def extract_codes(self):
        """从图片中提取股票代码"""
        # 读取图片
        img = cv2.imread(self.image_path)
        if img is None:
            print(f"无法读取图片: {self.image_path}")
            return []
        
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 二值化处理
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # 使用OCR识别
        text = pytesseract.image_to_string(binary, lang='chi_sim+eng', config='--psm 6')
        
        # 解析文本，提取第二列的股票代码
        lines = text.strip().split('\n')
        stock_codes = []
        
        for line in lines:
            # 分割每行内容，假设使用空格或制表符分隔
            parts = line.split()
            if len(parts) >= 2:
                # 第二列是股票代码
                code = parts[1]
                # 只保留数字和字母组成的股票代码
                if code.isalnum():
                    stock_codes.append(code)
        
        return stock_codes
    
    def save_to_file(self, codes, output_path="stock.txt"):
        """将股票代码保存到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for code in codes:
                f.write(code + '\n')
        print(f"已将{len(codes)}个股票代码保存到{output_path}")

if __name__ == "__main__":
    extractor = StockCodeExtractor("stock.jpg")
    codes = extractor.extract_codes()
    extractor.save_to_file(codes)
