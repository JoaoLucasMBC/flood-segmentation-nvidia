import re
from pathlib import Path

def load_env_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def update_version_in_paths(lines, version):
    updated_lines = []
    # Pattern to match "/v<digit>/" in paths
    version_pattern = re.compile(r'/v\d+/')

    for line in lines:
        if 'VERSION=' not in line:  # We don't want to modify the VERSION variable itself
            # Replace the version in the paths
            updated_line = version_pattern.sub(f'/v{version}/', line)
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)
    return updated_lines

def write_updated_env(file_path, updated_lines):
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

def main():
    env_file = '../config/.env'  # Change this to the path of your .env file if needed
    version = None
    # Load the .env file
    lines = load_env_file(env_file)

    # Find the VERSION variable
    for line in lines:
        if line.startswith('VERSION='):
            version = line.strip().split('=')[1]
            break

    if not version:
        print("VERSION variable not found in the .env file.")
        return

    # Update paths with the correct version
    updated_lines = update_version_in_paths(lines, version)

    # Write back the updated .env file
    write_updated_env(env_file, updated_lines)
    print(f".env file updated with version {version} in paths.")

if __name__ == '__main__':
    main()