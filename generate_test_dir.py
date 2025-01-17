import os
import subprocess
import yaml
from acl_script_framework import apply_acl_from_yaml, generate_yaml_template

# User and group for testing
TEST_USER = "sa_cs1cdk"
ANOTHER_USER = "cs1nmu"
TEST_GROUP = "el9testers"

def create_test_environment(base_dir):
    """
    Create a test directory structure with files and subdirectories.
    """
    try:
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"Created base directory: {base_dir}")

        # Generate subdirectories
        subdirs = ["subdir1", "subdir2/nested_subdir", "subdir3"]
        for subdir in subdirs:
            full_path = os.path.join(base_dir, subdir)
            os.makedirs(full_path, exist_ok=True)
            print(f"Created subdirectory: {full_path}")

            # Create random files in each subdirectory
            for i in range(3):
                filename = f"file_{i}.txt"
                file_path = os.path.join(full_path, filename)
                with open(file_path, "w") as f:
                    f.write(f"This is a test file in {subdir}\n")
                print(f"Created file: {file_path}")

    except Exception as e:
        print(f"Error creating test environment: {e}")

def get_acl_settings(path):
    """
    Retrieve ACL settings for a given path.
    """
    try:
        result = subprocess.run(["getfacl", "-R", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving ACL settings for {path}: {e.stderr}")
        return None

if __name__ == "__main__":
    base_test_dir = os.getenv("TMPDIR")
    if not base_test_dir:
        raise EnvironmentError("TMPDIR environment variable is not set.")

    base_test_dir = os.path.join(base_test_dir, "acl_test_environment")
    create_test_environment(base_test_dir)
    print(f"Test environment created at: {base_test_dir}")

    # Generate YAML template for testing
    yaml_file = os.path.join(base_test_dir, "acl_template.yaml")
    generate_yaml_template(yaml_file)
    print(f"Generated YAML template at: {yaml_file}")

    # View initial ACL settings
    print("\nInitial ACL settings:")
    initial_acl = get_acl_settings(base_test_dir)
    if initial_acl:
        print(initial_acl)

    # Save initial ACL settings to a file
    initial_acl_file = os.path.join(base_test_dir, "initial_acl.txt")
    with open(initial_acl_file, "w") as f:
        if initial_acl:
            f.write(initial_acl)
    print(f"Initial ACL settings saved to: {initial_acl_file}")

    # Modify YAML file for testing
    with open(yaml_file, "r") as f:
        acl_config = yaml.safe_load(f)

    acl_config["target_directory"] = base_test_dir
    acl_config["permissions"] = [ 
        {"user": TEST_USER, "permissions": "rwx"},
        {"group": TEST_GROUP, "permissions": "r-x"},
        {"user": ANOTHER_USER, "permissions": "rw-"}
    ]

    with open(yaml_file, "w") as f:
        yaml.dump(acl_config, f, default_flow_style=False, sort_keys=False, indent=2)
    print("Modified YAML configuration for testing.")

    # Apply ACLs from modified YAML
    apply_acl_from_yaml(yaml_file)

    # View ACL settings after changes
    print("\nACL settings after changes:")
    updated_acl = get_acl_settings(base_test_dir)
    if updated_acl:
        print(updated_acl)

    # Save updated ACL settings to a file
    updated_acl_file = os.path.join(base_test_dir, "updated_acl.txt")
    with open(updated_acl_file, "w") as f:
        if updated_acl:
            f.write(updated_acl)
    print(f"Updated ACL settings saved to: {updated_acl_file}")

    # Compare initial and updated ACL settings
    if initial_acl and updated_acl:
        if initial_acl == updated_acl:
            print("\nNo changes detected in ACL settings.")
        else:
            print("\nDifferences in ACL settings detected:")
            initial_lines = initial_acl.splitlines()
            updated_lines = updated_acl.splitlines()
            for line in set(updated_lines).difference(initial_lines):
                print(f"+ {line}")
            for line in set(initial_lines).difference(updated_lines):
                print(f"- {line}")

