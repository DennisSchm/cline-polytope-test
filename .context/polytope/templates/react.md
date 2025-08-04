# Directives for Creating a React App with Polytope

## CRITICAL: Always generate and customize components, never just create setup scripts!

When asked to create a React component as part of a larger task:
1. **ALWAYS** run the scaffold command to generate the component if an appropiate template is available 
2. **ALWAYS** add required packages using the component's add module
3. **ALWAYS** customize the generated code to meet the specific requirements
4. **NEVER** just create a setup script and leave component generation to the user

## Creating the component
**CRITICAL**: ALWAYS make sure that the template argument points inside the `.templates/` directory!

Use the build-in `polytope/scaffold` module to create a starting project via:
`pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'my-component-name'}"`

**Parameter explanation:**
- `template`: Points to the path where the template is stored (e.g., `.templates/frontend`)
- `path`: Points to the directory where the new project will be created

### Examples:
- Frontend component: `pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'frontend'}"`
- Another frontend: `pt run --non-interactive "polytope/scaffold{template: '.templates/frontend', path: 'web-app'}"`

## Adding packages to React components
Each React component created with the template includes a custom `{component-name}-add` module for adding packages.

**IMPORTANT**: The add module is only available AFTER the component has been generated and the main polytope.yml includes the component's polytope.yml file.

**Usage:**
```bash
pt run --non-interactive "{component-name}-add{packages: 'package-name'}"
```

**Examples:**
- For a 'frontend' component: `pt run --non-interactive "frontend-add{packages: 'axios'}"`
- For a 'web-app' component: `pt run --non-interactive "web-app-add{packages: 'react-query'}"`
- Multiple packages: `pt run --non-interactive "frontend-add{packages: 'axios react-query'}"`

**IMPORTANT:** 
- Do NOT specify package versions unless specifically requested by the user
- Use space-separated package names for multiple packages
- The packages parameter accepts comma or whitespace-separated lists

## After generating components
1. Update the main polytope.yml to include the generated component's polytope.yml file using the `include` directive
2. Customize the generated code files to implement the specific functionality required (forms, API calls, etc.)
3. Update configuration files as needed

## Dependencies
This creates a project based on bun and React with React Router v7.
