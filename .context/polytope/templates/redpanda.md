<instructions>
<title>Documentation on how to use Redpanda in Polytope</title>

<dev_mode_setup>
<section_title>Dev Mode and Topic Creation</section_title>
When configuring and running redpanda as described in this documentation, it runs in dev mode and creates topics lazily. **No setup to generate topics is needed** - topics are automatically created when first accessed.
</dev_mode_setup>

<component_creation>
<section_title>Creating Redpanda Components</section_title>
Use the redpanda template to automatically generate pre-configured redpanda components. This eliminates the need to manually configure redpanda modules in the root polytope file.

<generate_component>
<subsection_title>Generate a Redpanda Component</subsection_title>
Execute the following command in the terminal to use the polytope scaffold command with the redpanda template:
`pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'redpanda'}"`

<examples>
<example_title>Examples</example_title>

Server component 
`pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'redpanda'}"`

Another server
`pt run --raw "polytope/scaffold{template: '.templates/redpanda', path: 'server'}"`
</examples>

<generated_features>
The generated component includes:
- Pre-configured `polytope.yml` file with redpanda and redpanda console modules
- Proper persistent volume configuration
- All necessary wrapper modules

**IMPORTANT:** The generated `polytope.yml` file is pre-configured and should not be modified unless you need to change the Redpanda cluster configuration.
</generated_features>
</generate_component>
</component_creation>

<console_usage>
<section_title>Running Redpanda Console</section_title>
Run the `polytope/redpanda!console` module together with the redpanda server.

This defaults to connecting to the redpanda server running via `polytope/redpanda`, so there's no need to specify any args. Don't try to create a module wrapping this, you'll just trip yourself up.
</console_usage>

<python_integration>
<section_title>For any Python code that accesses redpanda</section_title>
Use the kafka-python package. Version: 2.2.15

You must check that no python code uses any other version of the kafka-python package.
</python_integration>
</instructions>
