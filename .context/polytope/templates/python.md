<instructions>
<title>Directives for Creating A Python Component</title>

<critical_workflow>
<rule>CRITICAL: Always generate and customize components, never just create setup scripts!</rule>

When asked to create a Python component as part of a larger task:
1. **ALWAYS** run the scaffold command to generate the component if an appropiate template is available
2. **ALWAYS** add required packages using the component's add module
3. **ALWAYS** customize the generated code to meet the specific requirements
4. **NEVER** just create a setup script and leave component generation to the user
</critical_workflow>

<component_creation>
<section_title>Creating the component</section_title>
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Execute the following command in the terminal to use the build-in `polytope/scaffold` module to create a starting project via:
`pt run --raw "polytope/scaffold{template: '.templates/python-api', path: 'my-component-name'}"`

<parameter_explanation>
**Parameter explanation:**
- `template`: Points to the path where the template is stored (e.g., `.templates/python-api`)
- `path`: Points to the directory where the new project will be created
</parameter_explanation>

<examples>
<subsection_title>Examples:</subsection_title>

API component
`pt run --raw "polytope/scaffold{template: '.templates/python-api', path: 'api'}"`

Another API
`pt run --raw "polytope/scaffold{template: '.templates/python-api', path: 'backend'}"`
</examples>
</component_creation>

<package_management>
<section_title>Adding packages to Python components</section_title>
Each Python component created with the template includes a custom `{component-name}-add` module for adding packages.

**IMPORTANT**: The add module is only available AFTER the component has been generated and the main polytope.yml includes the component's polytope.yml file.

<usage>
**Usage:**
Execute the following command in the terminal to add packages to template project.

`pt run --raw "{component-name}-add{packages: 'package-name'}"`
</usage>

<package_examples>
<subsection_title>Examples</subsection_title>
Execute the following commands in the terminal to add packages to your api project.

For an 'api' component
`pt run --raw "api-add{packages: 'kafka-python'}"`

For a 'backend' component
`pt run --raw "backend-add{packages: 'redis'}"`

Multiple packages
`pt run --raw "api-add{packages: 'kafka-python requests'}"`
</package_examples>

<package_guidelines>
**IMPORTANT:** 
- Do NOT specify package versions unless specifically requested by the user
- Use space-separated package names for multiple packages
- The packages parameter accepts comma or whitespace-separated lists
</package_guidelines>
</package_management>

<post_generation>
<section_title>After generating components</section_title>
1. Update the main polytope.yml to include the generated component's polytope.yml file using the `include` directive
2. Customize the generated code files to implement the specific functionality required
3. Update configuration files as needed
</post_generation>

<recommended_packages>
<section_title>Specific packages to use</section_title>
For api servers, use fastapi with uvicorn.

For real-time applications with WebSockets and message queues, see the **Real-time Application Patterns** guide in `.context/polytope/templates/realtime-patterns.md` for critical event loop integration patterns.
</recommended_packages>
</instructions>
