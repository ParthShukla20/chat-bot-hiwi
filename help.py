import re

output_text = "[doc1] This is the first document. [doc2] This is the second document. [doc3] This is the third document."

output_text = re.sub(r'\[doc(\d+)\]','\b\b', output_text)

print(output_text)