<instructions>
<title>Documentation on how to use PostgreSQL in Polytope</title>

<dev_mode_setup>
<section_title>Dev Mode and Database Creation</section_title>
When configuring and running PostgreSQL as described in this documentation, it runs in dev mode with automatic database initialization. **No manual setup for database creation is needed** - databases and schemas are automatically created when first accessed through migrations or application code.
</dev_mode_setup>

<component_creation>
<section_title>Creating PostgreSQL Components</section_title>
Use the postgres template to automatically generate pre-configured PostgreSQL components. This eliminates the need to manually configure postgres modules in the root polytope file.

<generate_component>
<subsection_title>Generate a PostgreSQL Component</subsection_title>
Execute the following command in the terminal to use the polytope scaffold command with the postgres template:
`pt run --raw "polytope/scaffold{template: '.templates/postgres', path: 'postgres'}"`

<examples>
<example_title>Examples</example_title>

Database server component 
`pt run --raw "polytope/scaffold{template: '.templates/postgres', path: 'postgres'}"`

Another database server
`pt run --raw "polytope/scaffold{template: '.templates/postgres', path: 'database'}"`
</examples>

<generated_features>
The generated component includes:
- Pre-configured `polytope.yml` file with postgres simple module
- Proper persistent volume configuration for data storage
- Environment variables for database connection
- All necessary wrapper modules

**IMPORTANT:** The generated `polytope.yml` file is pre-configured and should not be modified unless you need to change the PostgreSQL server configuration.
</generated_features>
</generate_component>
</component_creation>

<simple_module_usage>
<section_title>Using PostgreSQL Simple Module</section_title>
Use the `polytope/postgres!simple` module for basic PostgreSQL functionality.

This module provides a simple PostgreSQL server with:
- Default database initialization
- Standard PostgreSQL port (5432)
- Persistent data storage
- Ready-to-use connection parameters

Don't try to create complex wrapper modules around this, you'll just complicate the setup.
</simple_module_usage>

<connection_details>
<section_title>Database Connection Information</section_title>
When using the postgres simple module, the following connection details are available:
- **Host**: localhost (when running locally)
- **Port**: 5432 (default PostgreSQL port)
- **Database**: postgres (default database)
- **Username**: postgres (default user)
- **Password**: Available through environment variables or module configuration

These connection parameters are automatically configured by the polytope/postgres!simple module.
</connection_details>

<database_initialization_timing>
<section_title>Database Initialization Timing</section_title>
**CRITICAL:** Initialize database schema at application startup, not in WebSocket handlers or runtime events. This prevents "relation does not exist" errors when REST endpoints are accessed before WebSocket connections.

```python
# CORRECT: Initialize at module import time
def init_database():
    for attempt in range(10):
        try:
            # Database connection and schema creation
            break
        except Exception as e:
            if attempt < 9:
                time.sleep(2)
            else:
                raise

# Call at module level
init_database()
```
</database_initialization_timing>
</instructions>
