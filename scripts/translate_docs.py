#!/usr/bin/env python3
import os, re, argparse, shutil, time
from googletrans import Translator

class MarkdownTranslator:
    def __init__(self):
        self.translator = Translator()
        self.placeholders = {}
        self.tech_terms = ['ROS 2', 'DDS', 'Humble', 'Iron', 'Jazzy', 'CARET', 'caret', 'rclcpp', 'LTTng', 'Recording', 'recording']

    def _replace_with_placeholder(self, m):
        p = f"[[_FIX_ID_{len(self.placeholders)}_]]"
        self.placeholders[p] = m.group(0)
        return p

    def protect_structure(self, text):
        self.placeholders = {}
        text = re.sub(r'!?\[.*?\]\(.*?\)', self._replace_with_placeholder, text)
        text = re.sub(r'`[^`\n]+`', self._replace_with_placeholder, text)
        text = re.sub(r'<[^>]+>', self._replace_with_placeholder, text)
        for term in self.tech_terms:
            text = re.compile(rf'\b{term}\b', re.IGNORECASE).sub(self._replace_with_placeholder, text)
        return text

    def restore_structure(self, translated):
        for p, original in self.placeholders.items():
            pattern = p.replace("[[", r"\[\s*\[").replace("]]", r"\]\s*\]").replace("_", r"\s*_\s*")
            translated = re.sub(pattern, original, translated)
        return translated

    def translate_line(self, indent, content):
        if not content.strip(): return indent + content
        protected = self.protect_structure(content)
        try:
            time.sleep(0.1)
            t = self.translator.translate(protected, dest='ja')
            return indent + self.restore_structure(t.text).strip() + '\n'
        except: return indent + content

    def is_special_line(self, s):
        # 記号判定を簡略化
        if not s: return True
        # 行頭の数文字で判定
        head3 = s[:3]
        if head3 in [':::', '===', '!!!', '<!-']: return True
        if s[:2] == './': return True
        if s[:6] == 'export': return True
        return False

    def process_file(self, src, dst):
        with open(src, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        results = []
        in_fence = False
        for line in lines:
            stripped = line.lstrip()
            indent = line[:len(line)-len(stripped)]
            if stripped[:3] == '```':
                in_fence = not in_fence
                results.append(line)
                continue
            if in_fence or self.is_special_line(stripped.strip()):
                results.append(line)
            else:
                results.append(self.translate_line(indent, stripped))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w', encoding='utf-8') as f:
            f.writelines(results)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('src')
    p.add_argument('dst')
    args = p.parse_args()
    engine = MarkdownTranslator()
    for root, _, files in os.walk(args.src):
        for f in files:
            s_path = os.path.join(root, f)
            rel = os.path.relpath(s_path, args.src)
            d_path = os.path.join(args.dst, rel)
            if f.lower() == 'changelog.md':
                os.makedirs(os.path.dirname(d_path), exist_ok=True)
                shutil.copy2(s_path, d_path)
                continue
            if f.endswith('.md'):
                print(f"Translating: {rel}")
                engine.process_file(s_path, d_path)
            else:
                os.makedirs(os.path.dirname(d_path), exist_ok=True)
                shutil.copy2(s_path, d_path)

if __name__ == '__main__':
    main()
