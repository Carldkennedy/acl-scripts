import yaml
import os
import subprocess

def generate_yaml_template(output_file):
    """
    Generate a YAML template for ACL configurations.
    """
    template = {
        "target_directory": "/path/to/target_dir",
        "permissions": [
            {"user": "USERNAME", "permissions": "rwx"},
            {"group": "GROUPNAME", "permissions": "r-x"}
        ],
        "per_dir_permissions": [
            {
                "path": "subdir1",
                "permissions": [
                    {"user": "ANOTHERUSER", "permissions": "rw-"}
                ]
            },
            {
                "path": "subdir2/nested_subdir",
                "permissions": [
                    {"user": "NEWUSER", "permissions": "r--"}
                ]
            }
        ],
        "apply_to": {
            "directories": True,
            "files": True,
            "default": True
        }
    }

    with open(output_file, 'w') as f:
        yaml.dump(template, f, default_flow_style=False, sort_keys=False, indent=2)
    print(f"YAML template written to {output_file}")

def apply_acl_from_yaml(yaml_file):
    """
    Apply ACL settings from a YAML configuration file.
    """
    # Load the YAML file
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    target_dir = config.get("target_directory")
    if not target_dir or not os.path.exists(target_dir):
        raise ValueError("Invalid or non-existent target directory specified in YAML.")

    permissions = config.get("permissions", [])
    per_dir_permissions = config.get("per_dir_permissions", [])
    apply_to = config.get("apply_to", {})

    # Apply general permissions
    for perm in permissions:
        entity = None
        if "user" in perm:
            entity = f"u:{perm['user']}"
        elif "group" in perm:
            entity = f"g:{perm['group']}"
    
        if entity:
            acl_rule = f"{entity}:{perm['permissions']}"
        else:
            print(f"Skipping invalid permission entry: {perm}")
            continue
    
        # Apply to existing directories and files
        if apply_to.get("directories", False):
            subprocess.run(["setfacl", "-Rm", acl_rule, target_dir], check=True)
        if apply_to.get("files", False):
            subprocess.run(["setfacl", "-Rm", acl_rule, target_dir], check=True)
    
        # Apply as default ACL
        if apply_to.get("default", False):
            subprocess.run(["setfacl", "-Rdm", acl_rule, target_dir], check=True)
    
    # Apply per-directory permissions
    for entry in per_dir_permissions:
        subdir = os.path.join(target_dir, entry.get("path", ""))
        if not os.path.exists(subdir):
            print(f"Warning: Subdirectory {subdir} does not exist. Skipping.")
            continue

        for perm in entry.get("permissions", []):
            if "user" in perm:
                entity = f"u:{perm['user']}"
            elif "group" in perm:
                entity = f"g:{perm['group']}"
            else:
                continue

        # Skip if neither user nor group is defined
        if not entity:
            print(f"Skipping invalid permission entry: {perm}")
            continue
            acl_rule = f"{entity}:{perm['permissions']}"
            acl_rule = f"{entity}:{perm['permissions']}"

            # Apply ACL to the specific subdirectory
            subprocess.run([
                "setfacl", "-Rm", acl_rule, subdir
            ], check=True)
            subprocess.run([
                "setfacl", "-Rdm", acl_rule, subdir
            ], check=True)

    print("ACLs applied successfully from YAML.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ACL Framework for POSIX Systems")
    parser.add_argument("--generate-template", help="Generate a YAML template for ACL settings", action="store_true")
    parser.add_argument("--apply", help="Apply ACLs from a YAML configuration file", type=str)
    args = parser.parse_args()

    if args.generate_template:
        generate_yaml_template("acl_template.yaml")
    elif args.apply:
        apply_acl_from_yaml(args.apply)
    else:
        parser.print_help()

