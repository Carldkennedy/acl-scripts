# ACL Scripts

This repository contains two Python scripts designed for generating and testing Access Control List (ACL) configurations in POSIX-compliant systems. These scripts help automate the creation of test environments, application of ACL rules, and verification of changes.

## Files in the Repository

### 1. `acl_script_framework.py`
A reusable framework for generating ACL configuration templates and applying ACL rules based on a YAML configuration file.

#### Features:
- **Template Generation**: Creates a YAML template for ACL configurations.
- **Apply ACLs**: Reads ACL rules from a YAML file and applies them to the specified directory and its contents.
- **Recursive and Default ACL Support**: By setting `recursive: true` in the YAML file, ACLs can be applied to all existing subdirectories and files,
ensuring consistent permissions throughout the directory tree. Default ACLs ensure newly created files inherit the correct permissions.

#### Key Functions:
- `generate_yaml_template(output_file)`: Generates a YAML template with placeholders for user and group permissions.
- `apply_acl_from_yaml(yaml_file)`: Applies ACL rules based on the provided YAML configuration.

#### Usage:
- Generate a YAML template:
  ```bash
  python acl_script_framework.py --generate-template
  ```
- Apply ACL rules from a YAML file:
  ```bash
  python acl_script_framework.py --apply <path_to_yaml>
  ```

Before making changes to ACLs it is advisable to backup the current ACL settings using ``getfacl``. This enables restoration in case of mistakes.

   ```bash
   getfacl -R /full/path/to/directory > acl_backup.txt
   # To reapply backed-up ACLs:
   setfacl --restore=acl_backup.txt
   ```

### 2. `generate_test_dirs.py`
A script to create a test environment with directories, files, and ACL settings for testing purposes.

#### Features:
- Creates a nested directory structure with test files.
- Reads and applies ACL rules using `acl_script_framework.py`.
- Compares and saves ACL settings before and after applying changes.

#### Key Functions:
- `create_test_environment(base_dir)`: Sets up a test directory structure.
- `get_acl_settings(path)`: Retrieves ACL settings for a specified path.

#### Usage:
1. Set the `TMPDIR` environment variable to a writable temporary directory (e.g, if in an interactive session on Stanage or Bessemer $TMPDIR will already be set).
2. Run the script:
   ```bash
   python generate_test_dirs.py
   ```

## Workflow
1. **Setup**:
   - Use `generate_test_dirs.py` to create a test environment and generate a YAML configuration file.
2. **Modify YAML**:
   - Update the YAML file with the desired ACL rules (e.g., users, groups, permissions).
3. **Apply ACLs**:
   - Use `apply_acl_from_yaml` to apply the updated ACL rules.
4. **Verify Changes**:
   - Compare and save ACL settings before and after the changes.

## Example YAML Configuration
```yaml
target_directory: /path/to/target_dir
permissions:
  - user: testuser
    permissions: rwx
  - group: testgroup
    permissions: r-x
  - user: anotheruser
    permissions: rw-
apply_to:
  directories: true
  files: true
  default: true
```

By setting `recursive: true`, the script will apply ACLs to all existing directories and files under the target directory, as well as set default ACLs for newly created files and directories.

```yaml
target_directory: /path/to/target_dir
permissions:
  - user: testuser
    permissions: rwx
  - group: testgroup
    permissions: r-x
  - user: anotheruser
    permissions: rw-
recursive: true
apply_to:
  directories: true
  files: true
  default: true
```

## Requirements
- Python 3.6+
- `getfacl` and `setfacl` commands available on the system.

## Outputs
- `initial_acl.txt`: Saved ACL settings before changes.
- `updated_acl.txt`: Saved ACL settings after changes.
- Console output detailing applied changes and differences.

## License
This repository is licensed under the MIT License. See the LICENSE file for details.

## Contributions
Feel free to open issues or submit pull requests for improvements or bug fixes.


