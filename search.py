import subprocess
import argparse
from typing import List, Dict

class FileSearcher:
    @staticmethod
    def find_files(query: str) -> List[str]:
        """Search filenames using exa"""
        cmd = f"exa --tree --color=never | grep -i '{query}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [line.strip() for line in result.stdout.split('\n') if line]

    @staticmethod
    def grep_content(query: str) -> Dict[str, List[str]]:
        """Search file contents using grep"""
        cmd = f"grep -rni --color=never '{query}' ."
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        matches = {}
        for line in result.stdout.split('\n'):
            if not line: continue
            file, _, content = line.partition(':')
            matches.setdefault(file, []).append(content.strip())
        
        return matches

class SearchCLI:
    def __init__(self):
        self.searcher = FileSearcher()
    
    def run(self):
        parser = argparse.ArgumentParser(description="Search Engine v1.0")
        parser.add_argument("query", help="Search term")
        parser.add_argument("-c", "--content", action="store_true", 
                          help="Search inside files")
        args = parser.parse_args()

        print(f"\n🔍 Searching for: '{args.query}'")
        
        files = self.searcher.find_files(args.query)
        print(f"\n📂 Found {len(files)} matching files:")
        for f in files:
            print(f"  - {f}")

        if args.content:
            contents = self.searcher.grep_content(args.query)
            print(f"\n📝 Found {len(contents)} files with matching content:")
            for file, matches in contents.items():
                print(f"\n{file}:")
                for m in matches:
                    print(f"  • {m}")

if __name__ == "__main__":
    SearchCLI().run()