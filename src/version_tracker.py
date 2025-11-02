#!/usr/bin/env python3

import json
import logging
import argparse
import os
from datetime import datetime
from github import Github

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

class VersionTracker:
    def __init__(self, github_token):
        self.github = Github(github_token)
        self.version_file = "last_component_versions.json"
    
    def get_current_versions(self, settings):
        """Get current versions of all components"""
        versions = {}
        
        for module_name, module_config in settings["moduleList"].items():
            try:
                repo = self.github.get_repo(module_config["repo"])
                releases = repo.get_releases()
                
                if releases.totalCount > 0:
                    latest_release = releases[0]
                    versions[module_name] = {
                        "version": latest_release.tag_name,
                        "published_at": latest_release.published_at.isoformat(),
                        "repo": module_config["repo"],
                        "url": latest_release.html_url
                    }
                else:
                    # Fallback to latest commit
                    commits = repo.get_commits()
                    if commits.totalCount > 0:
                        latest_commit = commits[0]
                        versions[module_name] = {
                            "version": f"commit-{latest_commit.sha[:7]}",
                            "published_at": latest_commit.commit.author.date.isoformat(),
                            "repo": module_config["repo"],
                            "url": latest_commit.html_url
                        }
                        
            except Exception as e:
                logging.warning(f"Failed to get version for {module_name}: {e}")
                versions[module_name] = {
                    "version": "unknown",
                    "published_at": datetime.now().isoformat(),
                    "repo": module_config["repo"],
                    "url": f"https://github.com/{module_config['repo']}"
                }
        
        return versions
    
    def load_previous_versions(self):
        """Load previous version information"""
        if not os.path.exists(self.version_file):
            return {}
        
        try:
            with open(self.version_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load previous versions: {e}")
            return {}
    
    def save_current_versions(self, versions):
        """Save current versions for next comparison"""
        try:
            with open(self.version_file, 'w') as f:
                json.dump(versions, f, indent=2)
            logging.info(f"Saved current versions to {self.version_file}")
        except Exception as e:
            logging.error(f"Failed to save versions: {e}")
    
    def find_updates(self, current_versions, previous_versions):
        """Find what components have been updated"""
        updates = {
            "new": [],      # New components
            "updated": [],  # Updated components
            "unchanged": [] # Unchanged components
        }
        
        for module_name, current_info in current_versions.items():
            if module_name not in previous_versions:
                updates["new"].append({
                    "name": module_name,
                    "version": current_info["version"],
                    "repo": current_info["repo"],
                    "url": current_info["url"]
                })
            elif previous_versions[module_name]["version"] != current_info["version"]:
                updates["updated"].append({
                    "name": module_name,
                    "old_version": previous_versions[module_name]["version"],
                    "new_version": current_info["version"],
                    "repo": current_info["repo"],
                    "url": current_info["url"]
                })
            else:
                updates["unchanged"].append({
                    "name": module_name,
                    "version": current_info["version"],
                    "repo": current_info["repo"]
                })
        
        return updates
    
    def generate_changelog(self, settings, updates):
        """Generate a focused changelog based on actual updates"""
        current_version = settings.get("releaseVersion", "unknown")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        notes = []
        notes.append(f"# Ascent v{current_version}")
        notes.append(f"*Released on {current_date}*")
        notes.append("")
        
        # Show what's been updated
        if updates["updated"] or updates["new"]:
            notes.append("## 🚀 What's Updated")
            notes.append("")
            
            if updates["updated"]:
                notes.append("### Updated Components")
                for item in updates["updated"]:
                    notes.append(f"- **{item['name']}**: `{item['old_version']}` → [`{item['new_version']}`]({item['url']}) - {item['repo']}")
                notes.append("")
            
            if updates["new"]:
                notes.append("### New Components")
                for item in updates["new"]:
                    notes.append(f"- **{item['name']}**: [`{item['version']}`]({item['url']}) - {item['repo']}")
                notes.append("")
        else:
            notes.append("## 📦 Package Update")
            notes.append("")
            notes.append("This release contains the same component versions as the previous release, but may include:")
            notes.append("- Build script improvements")
            notes.append("- Configuration updates") 
            notes.append("- Package structure optimizations")
            notes.append("")
        
        # Package information
        notes.append("## 📋 Available Packages")
        notes.append("")
        
        for package in settings.get("packages", []):
            if package.get("active", False):
                component_count = len(package.get("modules", []))
                notes.append(f"- **{package['name'].title()}**: {component_count} components")
        
        notes.append("")
        
        # Installation
        notes.append("## 📥 Installation")
        notes.append("")
        notes.append("1. Download the appropriate package for your setup")
        notes.append("2. Extract to the root of your Switch SD card")
        notes.append("3. Boot CFW using your preferred method")
        notes.append("")
        
        # Important info
        notes.append("## ⚠️ Important")
        notes.append("")
        notes.append("- Always backup your NAND before updating CFW")
        notes.append("- This is an automated build from the latest component releases")
        notes.append("")
        
        # Show all current versions in a collapsible section
        notes.append("<details>")
        notes.append("<summary>📦 Complete Component List (Click to expand)</summary>")
        notes.append("")
        
        all_components = updates["updated"] + updates["new"] + updates["unchanged"]
        all_components.sort(key=lambda x: x["name"])
        
        for item in all_components:
            version = item.get("new_version", item.get("version", "unknown"))
            notes.append(f"- **{item['name']}**: `{version}` - {item['repo']}")
        
        notes.append("")
        notes.append("</details>")
        notes.append("")
        
        notes.append("---")
        notes.append(f"*Generated automatically by [Ascent](https://github.com/exploitz86/Ascent) on {current_date}*")
        
        return "\n".join(notes)

def main():
    parser = argparse.ArgumentParser(description="Generate changelog based on component updates")
    parser.add_argument('-gt', '--github-token', required=True, help='GitHub Token')
    parser.add_argument('-o', '--output', default='changelog.md', help='Output file')
    
    args = parser.parse_args()
    
    # Load settings
    try:
        with open('./settings.json', 'r') as f:
            settings = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load settings.json: {e}")
        return 1
    
    tracker = VersionTracker(args.github_token)
    
    # Get current and previous versions
    logging.info("Fetching current component versions...")
    current_versions = tracker.get_current_versions(settings)
    
    logging.info("Loading previous component versions...")
    previous_versions = tracker.load_previous_versions()
    
    # Find updates
    updates = tracker.find_updates(current_versions, previous_versions)
    
    logging.info(f"Found {len(updates['updated'])} updated, {len(updates['new'])} new, {len(updates['unchanged'])} unchanged components")
    
    # Generate changelog
    changelog = tracker.generate_changelog(settings, updates)
    
    # Save changelog
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(changelog)
        logging.info(f"Changelog saved to {args.output}")
    except Exception as e:
        logging.error(f"Failed to save changelog: {e}")
        return 1
    
    # Save current versions for next time
    tracker.save_current_versions(current_versions)
    
    return 0

if __name__ == '__main__':
    exit(main())