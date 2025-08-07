<instructions>
<title>Directives for Creating a React App with Polytope</title>

<critical_workflow>
<rule>CRITICAL: Always generate and customize components, never just create setup scripts!</rule>

When asked to create a React component as part of a larger task:
1. **ALWAYS** run the scaffold command to generate the component if an appropiate template is available 
2. **ALWAYS** add required packages using the component's add module
3. **ALWAYS** customize the generated code to meet the specific requirements
4. **NEVER** just create a setup script and leave component generation to the user
</critical_workflow>

<component_creation>
<section_title>Creating the component</section_title>
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Use the build-in `polytope/scaffold` module to create a starting project via:
`pt run --raw "polytope/scaffold{template: '.templates/frontend', path: 'my-component-name'}"`

<parameter_explanation>
**Parameter explanation:**
- `template`: Points to the path where the template is stored (e.g., `.templates/frontend`)
- `path`: Points to the directory where the new project will be created
</parameter_explanation>

<examples>
<subsection_title>Examples:</subsection_title>
- Frontend component: `pt run --raw "polytope/scaffold{template: '.templates/frontend', path: 'frontend'}"`
- Another frontend: `pt run --raw "polytope/scaffold{template: '.templates/frontend', path: 'web-app'}"`
</examples>
</component_creation>

<package_management>
<section_title>Adding packages to React components</section_title>
Each React component created with the template includes a custom `{component-name}-add` module for adding packages.

**IMPORTANT**: The add module is only available AFTER the component has been generated and the main polytope.yml includes the component's polytope.yml file.

<usage>
**Usage:**
Execute the following command in the terminal to add packages to your frontend app.

`pt run --raw "{component-name}-add{packages: 'package-name'}"`
</usage>

<package_examples>
<subsection_title>Examples</subsection_title>
Execute the following command in the terminal to add packages to your frontend app.

For a 'frontend' component
`pt run --raw "frontend-add{packages: 'axios'}"`

For a 'web-app' component
`pt run --raw "web-app-add{packages: 'react-query'}"`

Multiple packages
`pt run --raw "frontend-add{packages: 'axios react-query'}"`
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
2. Customize the generated code files to implement the specific functionality required (forms, API calls, etc.)
3. Update configuration files as needed
</post_generation>

<dependencies>
<section_title>Dependencies</section_title>
This creates a project based on bun and React with React Router v7.
</dependencies>
</instructions>
