from PyPDF2 import PdfReader, PdfWriter

# 输入输出路径
input_path = r"C:\Users\Ninininight\Desktop\MCM\MCM_book.pdf"
output_path = r"C:\Users\Ninininight\Desktop\MCM\linear_program.pdf"

# 选取页码（注意：页码从 0 开始计数）
pages_to_keep = [_ for _ in range(7,22)]  

reader = PdfReader(input_path)
writer = PdfWriter()

# 添加指定页面
for i in pages_to_keep:
    writer.add_page(reader.pages[i])

# 导出新PDF
with open(output_path, "wb") as f:
    writer.write(f)

print("✅ 已导出：", output_path)
