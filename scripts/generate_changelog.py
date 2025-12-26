#!/usr/bin/env python3
"""
Changelog Generator - Auto-populate changelog from git commit messages

This script reads commit messages from GitHub and generates changelog entries
using Conventional Commits format (feat:, fix:, docs:, chore:, etc.)

Usage:
    python scripts/generate_changelog.py [--since-tag v2.4.0] [--until-tag v2.5.0]
    python scripts/generate_changelog.py --recent 20  # Get last 20 commits
    python scripts/generate_changelog.py --draft      # Preview without writing
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import argparse


class CommitMessage:
    """Parse conventional commit messages"""

    def __init__(self, message: str, sha: str, date: str):
        self.full_message = message
        self.sha = sha[:8]  # Short SHA
        self.date = date[:10]  # YYYY-MM-DD
        self.parse()

    def parse(self):
        """Parse conventional commit format: type(scope): description"""
        lines = self.full_message.split("\n")
        first_line = lines[0]

        # Conventional commit pattern
        if ":" in first_line:
            parts = first_line.split(":", 1)
            type_part = parts[0].strip()
            description = parts[1].strip()

            # Extract type and optional scope
            if "(" in type_part and ")" in type_part:
                self.type = type_part[: type_part.index("(")].strip()
                self.scope = type_part[type_part.index("(") + 1 : type_part.index(")")]
            else:
                self.type = type_part.strip()
                self.scope = None

            self.description = description
            self.body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        else:
            # Non-conventional format
            self.type = "other"
            self.scope = None
            self.description = first_line
            self.body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

    def __repr__(self):
        scope = f" ({self.scope})" if self.scope else ""
        return f"[{self.type.upper()}{scope}] {self.description} ({self.sha})"


class ChangelogGenerator:
    """Generate changelog from commit history"""

    TYPE_SECTIONS = {
        "feat": "Added",
        "add": "Added",
        "feature": "Added",
        "fix": "Fixed",
        "bug": "Fixed",
        "docs": "Documentation",
        "style": "Changed",
        "refactor": "Changed",
        "perf": "Performance",
        "test": "Tests",
        "chore": "Maintenance",
        "ci": "CI/CD",
        "other": "Other",
    }

    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.commits: List[CommitMessage] = []
        self.organized: Dict[str, List[CommitMessage]] = {}

    def fetch_commits(self, count: int = 50) -> List[CommitMessage]:
        """Fetch recent commits from git log"""
        try:
            # Use git log to get commits
            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"--max-count={count}",
                    "--format=%H|%s|%ai",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            for line in result.stdout.strip().split("\n"):
                if line:
                    sha, subject, date = line.split("|", 2)
                    self.commits.append(CommitMessage(subject, sha, date))

            return self.commits
        except subprocess.CalledProcessError as e:
            print(f"Error fetching commits: {e}", file=sys.stderr)
            return []

    def organize_commits(self) -> Dict[str, List[CommitMessage]]:
        """Organize commits by type"""
        self.organized = {}
        for commit in self.commits:
            section = self.TYPE_SECTIONS.get(commit.type.lower(), "Other")
            if section not in self.organized:
                self.organized[section] = []
            self.organized[section].append(commit)
        return self.organized

    def format_section(self, section_name: str, commits: List[CommitMessage]) -> str:
        """Format a changelog section"""
        lines = [f"### {section_name}\n"]
        for commit in commits:
            lines.append(
                f"- {commit.description} ([{commit.sha}](https://github.com/{self.repo_owner}/{self.repo_name}/commit/{commit.sha}))"
            )
        return "\n".join(lines)

    def generate(self, version: str, date: str | None = None) -> str:
        """Generate changelog content"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        self.organize_commits()

        lines = [f"## [{version}] - {date}\n"]

        # Standard changelog section order
        section_order = [
            "Added",
            "Changed",
            "Fixed",
            "Performance",
            "Documentation",
            "Tests",
            "Maintenance",
            "CI/CD",
            "Other",
        ]

        for section in section_order:
            if section in self.organized and self.organized[section]:
                lines.append(self.format_section(section, self.organized[section]))
                lines.append("")  # Blank line between sections

        return "\n".join(lines)

    def preview(self, version: str, count: int = 20) -> None:
        """Preview changelog without writing"""
        print(f"\n📄 Preview: Changelog for v{version}\n")
        print(f"Found {len(self.commits)} commits\n")
        print(self.generate(version))


def main():
    parser = argparse.ArgumentParser(
        description="Generate changelog from git commit messages"
    )
    parser.add_argument(
        "--version",
        default="Unreleased",
        help="Version number for changelog entry (default: Unreleased)",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=20,
        help="Number of recent commits to include (default: 20)",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Preview changelog without writing to file",
    )
    parser.add_argument(
        "--output",
        default="CHANGELOG.md",
        help="Output file (default: CHANGELOG.md)",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing changelog (prepend new entry)",
    )

    args = parser.parse_args()

    # Initialize generator
    generator = ChangelogGenerator("KnowOneActual", "mail-ops-scripts")

    # Fetch commits
    print(f"Fetching {args.recent} recent commits...")
    generator.fetch_commits(count=args.recent)
    print(f"Found {len(generator.commits)} commits\n")

    if args.draft:
        generator.preview(args.version, args.recent)
        return

    # Generate changelog
    new_content = generator.generate(args.version)

    # Handle file writing
    output_path = Path(args.output)

    if args.append and output_path.exists():
        existing = output_path.read_text()
        content = new_content + "\n" + existing
        print(f"Appending to {output_path}...")
    else:
        content = new_content
        print(f"Creating new changelog: {output_path}...")

    output_path.write_text(content)
    print(f"\u2705 Changelog generated successfully!\n")
    print("Preview:")
    print(new_content)


if __name__ == "__main__":
    main()
